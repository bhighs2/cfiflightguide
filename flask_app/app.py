from pathlib import Path
from functools import lru_cache
import hashlib
import html
import os
import re
import tempfile
from urllib.parse import urlparse, parse_qs, urlencode, quote
from urllib.parse import (
    urlparse,
    parse_qs,
    urlencode,
    quote,
    unquote,
)

import markdown
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    send_file,
    send_from_directory,
)
from openai import OpenAI
from pypdf import PdfReader, PdfWriter

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parent
CONTENT_ROOT = PROJECT_ROOT / "content"
KNOWLEDGE_ROOT = PROJECT_ROOT / "knowledge" / "approved"
load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()

SITE_VECTOR_STORE_ID = os.getenv(
    "OPENAI_SITE_VECTOR_STORE_ID"
)

APPROVED_VECTOR_STORE_ID = os.getenv(
    "OPENAI_APPROVED_VECTOR_STORE_ID"
)

OPENAI_CHAT_MODEL = os.getenv(
    "OPENAI_CHAT_MODEL",
    "gpt-5"
)

# ---------------------------------------------------------
# FLASK
# ---------------------------------------------------------

app = Flask(__name__)


# ---------------------------------------------------------
# NAME / URL HELPERS
# ---------------------------------------------------------

DOCUMENT_DISPLAY_NAMES = {
    "Airplane_Flying_Handbook.pdf":
        "Airplane Flying Handbook",
    "Pilots_Handbook_of_Aeronautical_Knowledge.pdf":
        "Pilot's Handbook of Aeronautical Knowledge",
    "Aviation_Instructors_Handbook.pdf":
        "Aviation Instructor's Handbook",
    "Risk_Management_Handbook.pdf":
        "Risk Management Handbook",
    "POH-Cessna-172S.pdf":
        "Cessna 172S POH",
    "ACS_Private_Pilot.pdf":
        "Private Pilot ACS",
    "CFI_ASEL_ACS.pdf":
        "CFI Airplane ACS",
    "14_CFR_Part_43.pdf":
        "14 CFR Part 43",
    "14_CFR_Part_61.pdf":
        "14 CFR Part 61",
    "14_CFR_Part_91.pdf":
        "14 CFR Part 91",
    "AC_61-65K_Certification.pdf":
        "AC 61-65K",
    "Airworthiness_Checklist.pdf":
        "Airworthiness Checklist",
}


def pdf_document_display_name(url):
    """Return a friendly display name for an embedded PDF URL."""

    filename = Path(
        unquote(
            urlparse(url).path
        )
    ).name

    if filename in DOCUMENT_DISPLAY_NAMES:
        return DOCUMENT_DISPLAY_NAMES[filename]

    cleaned_name = re.sub(
        r"\.pdf$",
        "",
        filename,
        flags=re.IGNORECASE,
    )

    cleaned_name = re.sub(
        r"[_-]+",
        " ",
        cleaned_name,
    )

    return re.sub(
        r"\s+",
        " ",
        cleaned_name,
    ).strip() or "Reference Document"

def strip_numeric_prefix(name):
    """
    01_Solo_Qualification
    ->
    Solo_Qualification
    """

    if "_" in name:
        first, remainder = name.split("_", 1)

        if first.isdigit():
            return remainder

    return name


def display_name(name):
    """
    Folder name -> human-readable UI title.
    """

    name = strip_numeric_prefix(name)
    name = name.replace("_", " ")

    labels = {
        "private": "Private",
        "instrument": "Instrument",
        "commercial": "Commercial",
        "cfi": "CFI",
        "cfii": "CFII",
        "acs study guides": "ACS Study Guides",
        "training syllabi": "Training Syllabi",
    }

    return labels.get(
        name.lower(),
        name,
    )


def slugify(name):
    """
    Folder name -> URL segment.

    Important:
    private -> private
    cfi -> cfi

    This keeps URLs aligned with the canonical URLs
    already stored in the OpenAI vector store.
    """

    name = strip_numeric_prefix(name)
    name = name.replace("_", " ").lower()

    name = re.sub(
        r"[^a-z0-9]+",
        "-",
        name,
    )

    return name.strip("-")


def make_markdown_links_new_tab(html):
    return re.sub(
        r'<a\s+href=',
        '<a target="_blank" rel="noopener noreferrer" href=',
        html
    )

def parse_time_value(value):
    """
    Convert a media timestamp to seconds.

    Supported examples:

    342      -> 342
    342s     -> 342
    5m42s    -> 342
    05:42    -> 342
    1:05:42  -> 3942
    """

    if value is None:
        return None

    value = str(value).strip().lower()

    if not value:
        return None

    if value.isdigit():
        return int(value)

    if ":" in value:

        parts = value.split(":")

        if (
            len(parts) in {2, 3}
            and all(part.isdigit() for part in parts)
        ):

            numbers = [int(part) for part in parts]

            if len(numbers) == 2:
                minutes, seconds = numbers
                return minutes * 60 + seconds

            hours, minutes, seconds = numbers

            return (
                hours * 3600
                + minutes * 60
                + seconds
            )

    hours = re.search(r"(\d+)h", value)
    minutes = re.search(r"(\d+)m", value)
    seconds = re.search(r"(\d+)s", value)

    if not any([hours, minutes, seconds]):
        return None

    total = 0

    if hours:
        total += int(hours.group(1)) * 3600

    if minutes:
        total += int(minutes.group(1)) * 60

    if seconds:
        total += int(seconds.group(1))

    return total


def parse_embed_spec(raw_value):
    """
    Split a custom embed into its source and options.

    Example:

    URL | start=05:42 | end=08:39
    """

    parts = [
        part.strip()
        for part in raw_value.split("|")
    ]

    source = parts[0]
    options = {}

    for part in parts[1:]:

        if "=" not in part:
            continue

        key, value = part.split("=", 1)

        options[
            key.strip().lower()
        ] = value.strip()

    return source, options


def parse_positive_int(value):
    """
    Return a positive integer or None.
    """

    if value is None:
        return None

    try:
        number = int(str(value).strip())
    except (TypeError, ValueError):
        return None

    if number < 1:
        return None

    return number


def youtube_video_info(url):
    """
    Get the YouTube video ID and optional starting time.
    """

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    video_id = None

    # Standard YouTube URL:
    # https://www.youtube.com/watch?v=VIDEO_ID

    if "youtube.com" in parsed.netloc:

        if parsed.path == "/watch":
            video_id = query.get("v", [None])[0]

        elif parsed.path.startswith("/embed/"):
            video_id = (
                parsed.path
                .split("/embed/", 1)[1]
                .split("/")[0]
            )

        elif parsed.path.startswith("/shorts/"):
            video_id = (
                parsed.path
                .split("/shorts/", 1)[1]
                .split("/")[0]
            )

    # Short YouTube URL:
    # https://youtu.be/VIDEO_ID

    elif "youtu.be" in parsed.netloc:

        video_id = (
            parsed.path
            .strip("/")
            .split("/")[0]
        )

    start_value = (
        query.get("t", [None])[0]
        or query.get("start", [None])[0]
    )

    start_seconds = (
        parse_time_value(start_value)
        or 0
    )

    return video_id, start_seconds


def process_custom_embeds(markdown_text):
    """
    Custom Markdown extensions.

    Supported:

    [[youtube: URL]]

    [[youtube: URL | end=08:39]]

    [[youtube: URL | start=05:42 | end=08:39]]

    [[pdf: URL]]

    [[pdf: URL | start=39 | end=42]]

    [[mnemonic: DR DR F CPR | Denial · Repression · ...]]

    [[highlight:
    Attention |
    Important highlighted content here.
    ]]

    [[answer:
    Answer text here.
    ]]
    """

    # -----------------------------------------------------
    # YOUTUBE
    # -----------------------------------------------------

    youtube_pattern = r"\[\[youtube:\s*(.*?)\s*\]\]"

    def replace_youtube(match):

        raw_value = match.group(1)

        url, options = parse_embed_spec(
            raw_value
        )

        video_id, start_seconds = youtube_video_info(
            url
        )

        if not video_id:
            return f"[Invalid YouTube URL]({url})"

        if "start" in options:

            parsed_start = parse_time_value(
                options["start"]
            )

            if parsed_start is None:
                return "[Invalid YouTube start time]"

            start_seconds = parsed_start

        end_seconds = None

        if "end" in options:

            end_seconds = parse_time_value(
                options["end"]
            )

            if end_seconds is None:
                return "[Invalid YouTube end time]"

            if end_seconds <= start_seconds:
                return (
                    "[YouTube end time must be "
                    "after start time]"
                )

        safe_video_id = html.escape(
            video_id,
            quote=True,
        )

        safe_start = str(
            int(start_seconds)
        )

        safe_end = (
            str(int(end_seconds))
            if end_seconds is not None
            else ""
        )

        safe_title = html.escape(
            options.get(
                "title",
                "Video Excerpt",
            ),
            quote=False,
        )

        # The iframe itself is created by lesson.js through
        # YouTube's IFrame API.  We intentionally do not
        # expose YouTube's native scrub bar.  lesson.js
        # supplies a segment-relative progress control that
        # clamps seeking to start_seconds -> end_seconds.

        return f"""
<div
    class="youtube-segment"
    data-video-id="{safe_video_id}"
    data-start="{safe_start}"
    data-end="{safe_end}"
>
    <div class="youtube-segment-player-wrap">

        <div class="youtube-segment-player"></div>

        <div class="youtube-segment-cover">

            <img
                src="/static/branding/flight_guide_app_icon.png"
                alt="Flight Guide"
                class="youtube-segment-cover-icon"
            >

            <div class="youtube-segment-cover-title">
                Flight Guide
            </div>

            <div class="youtube-segment-cover-subtitle">
                {safe_title}
            </div>

        </div>

    </div>

    <div class="youtube-segment-controls">

        <button
            class="youtube-segment-play"
            type="button"
            aria-label="Play video excerpt"
        >
            ▶
        </button>

        <input
            class="youtube-segment-progress"
            type="range"
            min="0"
            max="1000"
            value="0"
            step="1"
            aria-label="Video excerpt progress"
        >

        <span class="youtube-segment-time">
            0:00 / 0:00
        </span>

    </div>
</div>
"""

    markdown_text = re.sub(
        youtube_pattern,
        replace_youtube,
        markdown_text
    )


    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    pdf_pattern = r"\[\[pdf:\s*(.*?)\s*\]\]"

    def replace_pdf(match):

        raw_value = match.group(1)

        url, options = parse_embed_spec(
            raw_value
        )

        start_raw = options.get("start")
        end_raw = options.get("end")

        start_page = parse_positive_int(
            start_raw
        )

        end_page = parse_positive_int(
            end_raw
        )

        if (
            start_raw is not None
            and start_page is None
        ):
            return "[Invalid PDF start page]"

        if (
            end_raw is not None
            and end_page is None
        ):
            return "[Invalid PDF end page]"

        clean_url = url.split("#", 1)[0]

        # If an end page is supplied, create a constrained
        # excerpt containing only the requested page range.

        if end_page is not None:

            if start_page is None:
                start_page = 1

            if end_page < start_page:
                return (
                    "[PDF end page must be greater than "
                    "or equal to start page]"
                )

            if not clean_url.startswith(
                "/knowledge/"
            ):
                return (
                    "[PDF page-range embeds require a "
                    "local /knowledge/ PDF]"
                )

            filename = clean_url[
                len("/knowledge/"):
            ]

            url = (
                "/knowledge-excerpt/"
                + quote(filename, safe="/")
                + f"?start={start_page}"
                + f"&end={end_page}"
            )

        elif start_page is not None:

            url = (
                clean_url
                + f"#page={start_page}"
            )

        if start_page is not None and end_page is not None:
            page_label = (
                f"Pages {start_page}–{end_page}"
            )
        elif start_page is not None:
            page_label = f"Page {start_page}"
        else:
            page_label = "Reference Document"

        safe_url = html.escape(
            url,
            quote=True,
        )

        safe_page_label = html.escape(
            page_label,
            quote=False,
        )

        safe_document_name = html.escape(
            pdf_document_display_name(
                clean_url
            ),
            quote=False,
        )

        return f"""
<div
    class="pdf-embed pdf-embed-lazy"
    data-pdf-src="{safe_url}"
>
    <button
        class="pdf-source-toggle"
        type="button"
        aria-expanded="false"
    >
        <span class="pdf-source-label">SOURCE</span>
        <span class="pdf-source-range">
            {safe_document_name}
            ·
            {safe_page_label}
        </span>
        <span class="pdf-source-action">View Source</span>
    </button>

    <div class="pdf-viewer" hidden></div>
</div>
"""

    markdown_text = re.sub(
        pdf_pattern,
        replace_pdf,
        markdown_text
    )


    # -----------------------------------------------------
    # MNEMONIC / MEMORY AID
    # -----------------------------------------------------

    mnemonic_pattern = (
        r"\[\[mnemonic:\s*(.*?)\s*\]\]"
    )

    def replace_mnemonic(match):

        raw_value = match.group(1).strip()

        if "|" in raw_value:
            mnemonic, expansion = (
                raw_value.split("|", 1)
            )
        else:
            mnemonic = raw_value
            expansion = ""

        mnemonic = html.escape(
            mnemonic.strip()
        )

        expansion = html.escape(
            expansion.strip()
        )

        expansion_html = ""

        if expansion:
            expansion_html = f"""
    <div class="lesson-mnemonic-expansion">
        {expansion}
    </div>
"""

        return f"""
<div class="lesson-mnemonic">
    <div class="lesson-mnemonic-label">
        Memory aid
    </div>
    <div class="lesson-mnemonic-code">
        {mnemonic}
    </div>
    {expansion_html}
</div>
"""

    markdown_text = re.sub(
        mnemonic_pattern,
        replace_mnemonic,
        markdown_text,
        flags=re.DOTALL,
    )

    # -----------------------------------------------------
    # HIGHLIGHT / IMPORTANT CONTENT
    # -----------------------------------------------------

    highlight_pattern = (
        r"\[\[highlight:\s*(.*?)\s*\]\]"
    )

    def replace_highlight(match):

        raw_value = (
            match.group(1)
            .strip()
        )

        if "|" in raw_value:

            label, content = (
                raw_value.split(
                    "|",
                    1,
                )
            )

        else:

            label = "Important"
            content = raw_value


        label = html.escape(
            label.strip()
        )


        content = (
            content.strip()
        )


        content_html = markdown.markdown(
            content,
            extensions=[
                "extra",
                "sane_lists",
            ],
        )


        return f"""
<div class="lesson-highlight">

    <div class="lesson-highlight-label">
        {label}
    </div>

    <div class="lesson-highlight-content">
        {content_html}
    </div>

</div>
"""


    markdown_text = re.sub(
        highlight_pattern,
        replace_highlight,
        markdown_text,
        flags=re.DOTALL,
    )

    # -----------------------------------------------------
    # HIDDEN / REVEALABLE ANSWERS
    # -----------------------------------------------------

    answer_pattern = (
        r"\[\[answer:\s*(.*?)\s*\]\]"
    )

    def replace_answer(match):

        answer_text = (
            match.group(1)
            .strip()
        )

        answer_html = markdown.markdown(
            answer_text,
            extensions=[
                "extra",
                "sane_lists",
            ],
        )

        return f"""
<details class="lesson-answer">
    <summary>Show Answer</summary>

    <div class="lesson-answer-content">
        {answer_html}
    </div>
</details>
"""

    markdown_text = re.sub(
        answer_pattern,
        replace_answer,
        markdown_text,
        flags=re.DOTALL,
    )


    return markdown_text

def get_current_lesson(current_path):
    """
    Given a site URL such as:

    /private/solo-qualification/test-lesson

    return:
        title
        markdown text
        canonical URL
    """

    if not current_path:
        return None

    clean_path = current_path.strip("/")

    if not clean_path:
        return None

    folder = resolve_content_folder(
        clean_path
    )

    lesson_file = folder / "lesson.md"

    if not lesson_file.is_file():
        return None

    return {
        "title": display_name(folder.name),
        "content": lesson_file.read_text(
            encoding="utf-8"
        ),
        "url": "/" + clean_path,
    }

def build_chat_instructions(scope):
    """
    Strict grounding rules for the aviation assistant.
    """

    instructions = """
You are the aviation training assistant for this website.

There are two types of knowledge available.

SITE CONTENT
This contains the user's actual Private Pilot and CFI website material.

APPROVED AVIATION SOURCES
These contain authoritative aviation references explicitly approved
by the site owner.

STRICT SOURCE RULES

1. Never claim that a lesson, section, page, syllabus item, document,
   video, or other website resource exists unless it is present in
   retrieved SITE CONTENT or has been supplied as the current lesson.

2. Never invent a website lesson or infer that one probably exists.

3. Previous assistant statements are NOT proof that a site resource exists.
   When discussing what exists in the library, rely on retrieved SITE CONTENT.

4. If the user asks where something exists and no relevant SITE CONTENT
   was retrieved, say clearly that you do not currently find that material
   in the site library.

5. Do not say things such as:
   "I can take you there",
   "I can open that",
   "You have a lesson on that",
   unless an actual SITE CONTENT result supports it.

6. Use APPROVED AVIATION SOURCES for aviation facts, procedures,
   regulations, standards, tolerances, aerodynamics, and technical explanations.

7. Do not use unsupported general aviation knowledge as authoritative fact.

8. Never invent an FAA citation, regulation, ACS requirement,
   document, page number, procedure, or tolerance.

9. If approved aviation material does not adequately support an answer,
   say that the approved knowledge currently available is insufficient.

10. If SITE CONTENT conflicts with APPROVED AVIATION SOURCES,
    identify the conflict and follow the authoritative source.

11. Be concise and practical.

12. Do not invent website URLs. The application generates navigation links
    separately from actual retrieval results.

13. Never display tool-call arguments, search-query JSON, internal
    retrieval commands, or other machine-readable tool syntax to the user.
    Always respond to the user in normal conversational language.

14. Support aviation factual answers with APPROVED AVIATION SOURCES
    whenever relevant. The application will display references from
    your actual file citations. Do not invent reference names,
    citations, page numbers, or source documents.
"""

    if scope == "lesson":
        instructions += """

CURRENT LESSON MODE

The exact current lesson content is supplied with the user's message.

When the user says:
- this lesson
- this page
- here
- this section
- the material above

they are referring to that supplied lesson.

You may summarize and discuss the supplied lesson directly.

Use APPROVED AVIATION SOURCES when aviation facts require verification
or additional authoritative explanation.

Do not claim that other site lessons exist unless they were actually
retrieved or otherwise supplied by the application.
"""

    return instructions.strip()

def extract_search_sources(response):
    """
    Extract useful links from OpenAI file-search results.

    SITE_CONTENT results become links back into this website.

    APPROVED_AVIATION_SOURCES results become links to the
    shared document under /knowledge/.
    """

    sources = []
    seen = set()

    for item in response.output:

        if getattr(item, "type", None) != "file_search_call":
            continue

        results = getattr(item, "results", None) or []

        for result in results:

            attributes = getattr(
                result,
                "attributes",
                None
            ) or {}

            source_type = attributes.get(
                "source_type"
            )

            title = (
                attributes.get("title")
                or getattr(result, "filename", None)
                or "Source"
            )

            url = None
            authority = None

            # ---------------------------------------------
            # SITE LESSON
            # ---------------------------------------------

            if source_type == "site":

                url = attributes.get(
                    "canonical_url"
                )

                authority = "Site Content"

            # ---------------------------------------------
            # APPROVED AVIATION SOURCE
            # ---------------------------------------------

            elif source_type == "authoritative":

                source_path = attributes.get(
                    "source_path"
                )

                if source_path:
                    url = (
                        "/knowledge/"
                        + source_path
                    )

                authority = (
                    attributes.get("authority")
                    or "Approved Source"
                )

            if not url:
                continue

            key = (
                source_type,
                url
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append({
                "title": title,
                "url": url,
                "type": source_type,
                "authority": authority,
            })

    return sources

def normalize_pdf_lookup_text(text):
    """
    Normalize text so small formatting differences between
    OpenAI's PDF extraction and pypdf extraction matter less.
    """

    if not text:
        return ""

    words = re.findall(
        r"[a-z0-9]+",
        text.lower()
    )

    return " ".join(words)


def make_word_shingles(text, size=5):
    """
    Convert normalized text into groups of consecutive words.
    """

    words = text.split()

    if len(words) < size:
        return set()

    return {
        tuple(words[i:i + size])
        for i in range(
            len(words) - size + 1
        )
    }


@lru_cache(maxsize=32)
def load_pdf_page_index(filename):
    """
    Load the locally generated page-aware text index.

    Example source:
        knowledge/index/
        Pilots_Handbook_of_Aeronautical_Knowledge.pdf.txt
    """

    index_path = (
        PROJECT_ROOT
        / "knowledge"
        / "index"
        / f"{filename}.txt"
    )

    if not index_path.exists():
        return []


    full_text = index_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


    page_markers = list(
        re.finditer(
            r"<<<PDF_PAGE:(\d+)>>>",
            full_text
        )
    )


    pages = []


    for i, marker in enumerate(
        page_markers
    ):

        page_number = int(
            marker.group(1)
        )

        start = marker.end()


        if i + 1 < len(page_markers):

            end = (
                page_markers[i + 1]
                .start()
            )

        else:

            end = len(full_text)


        page_text = (
            full_text[start:end]
        )

        normalized = (
            normalize_pdf_lookup_text(
                page_text
            )
        )

        shingles = (
            make_word_shingles(
                normalized
            )
        )


        pages.append({
            "page": page_number,
            "shingles": shingles,
        })


    return pages


def find_pdf_page(
    filename,
    retrieved_text,
):
    """
    Match an OpenAI File Search result against our
    local page-aware PDF index.

    Returns the physical PDF viewer page number.
    """

    normalized = (
        normalize_pdf_lookup_text(
            retrieved_text
        )
    )


    retrieved_shingles = (
        make_word_shingles(
            normalized
        )
    )


    if not retrieved_shingles:
        return None


    pages = load_pdf_page_index(
        filename
    )


    best_page = None
    best_hits = 0
    best_ratio = 0


    for page in pages:

        matches = (
            retrieved_shingles
            & page["shingles"]
        )

        hits = len(matches)

        ratio = (
            hits
            / len(retrieved_shingles)
        )


        if (
            hits > best_hits
            or (
                hits == best_hits
                and ratio > best_ratio
            )
        ):

            best_page = page["page"]
            best_hits = hits
            best_ratio = ratio


    # Require at least two matching
    # five-word sequences.
    #
    # If we cannot confidently locate it,
    # return no page rather than guess.

    if best_hits < 2:
        return None


    return best_page


def extract_response_references(
    response,
    lesson=None,
):
    """
    Return only files that the model actually cited
    in its generated response.

    File citation annotations contain file IDs.
    We map those IDs back to File Search results so
    we can recover canonical URLs and source metadata.
    """

    # -----------------------------------------------------
    # BUILD FILE LOOKUP FROM SEARCH RESULTS
    # -----------------------------------------------------

    file_lookup = {}

    for item in response.output:

        if getattr(
            item,
            "type",
            None
        ) != "file_search_call":
            continue

        results = getattr(
            item,
            "results",
            None
        ) or []

        for result in results:

            file_id = getattr(
                result,
                "file_id",
                None
            )

            if not file_id:
                continue

            attributes = getattr(
                result,
                "attributes",
                None
            ) or {}

            score = (
                getattr(
                    result,
                    "score",
                    0
                )
                or 0
            )

            candidate = {
                "filename": getattr(
                    result,
                    "filename",
                    None
                ),
                "attributes": attributes,

                "text": getattr(
                    result,
                    "text",
                    ""
                ) or "",

                "score": score,
            }


            existing = file_lookup.get(
                file_id
            )


            # A file can have multiple retrieved passages.
            # For this first test, retain the highest-scoring
            # passage from that file.

            if (
                existing is None
                or score > existing.get(
                    "score",
                    0
                )
            ):

                file_lookup[file_id] = (
                    candidate
                )


    # -----------------------------------------------------
    # FIND FILE CITATION ANNOTATIONS
    # -----------------------------------------------------

    cited_file_ids = []

    for item in response.output:

        if getattr(
            item,
            "type",
            None
        ) != "message":
            continue

        content_items = getattr(
            item,
            "content",
            None
        ) or []

        for content in content_items:

            if getattr(
                content,
                "type",
                None
            ) != "output_text":
                continue

            annotations = getattr(
                content,
                "annotations",
                None
            ) or []

            for annotation in annotations:

                if getattr(
                    annotation,
                    "type",
                    None
                ) != "file_citation":
                    continue

                file_id = getattr(
                    annotation,
                    "file_id",
                    None
                )

                if (
                    file_id
                    and file_id not in cited_file_ids
                ):
                    cited_file_ids.append(
                        file_id
                    )


    # -----------------------------------------------------
    # BUILD USER-FACING REFERENCES
    # -----------------------------------------------------

    references = []

    for file_id in cited_file_ids:

        info = file_lookup.get(
            file_id,
            {}
        )

        attributes = info.get(
            "attributes",
            {}
        )

        filename = (
            info.get("filename")
            or "Reference"
        )

        source_type = attributes.get(
            "source_type"
        )

        title = (
            attributes.get("title")
            or filename
        )

        url = None
        authority = None


        # -------------------------------------------------
        # SITE CONTENT
        # -------------------------------------------------

        if source_type == "site":

            url = attributes.get(
                "canonical_url"
            )

            authority = "Site Content"


        # -------------------------------------------------
        # APPROVED AVIATION SOURCE
        # -------------------------------------------------

        elif source_type == "authoritative":

            source_path = (
                attributes.get("source_path")
                or filename
            )


            retrieved_text = (
                info.get("text")
                or ""
            )


            pdf_page = find_pdf_page(
                filename,
                retrieved_text,
            )


            if source_path:

                url = (
                    "/knowledge/"
                    + source_path
                )


                if pdf_page:

                    url += (
                        f"#page={pdf_page}"
                    )


            if pdf_page:

                title = (
                    f"{title} — "
                    f"PDF p. {pdf_page}"
                )


            authority = (
                attributes.get("authority")
                or "Approved Aviation Source"
            )


        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------

        else:

            authority = (
                "Approved Aviation Source"
            )


        references.append({
            "title": title,
            "url": url,
            "type": source_type,
            "authority": authority,
            "file_id": file_id,
        })


    # -----------------------------------------------------
    # CURRENT LESSON
    # -----------------------------------------------------
    #
    # Current lesson text is passed directly to the model,
    # so OpenAI cannot generate a File Search citation for it.
    #
    # In lesson mode we therefore identify it explicitly
    # as contextual material.

    if lesson is not None:

        current_lesson_reference = {
            "title": lesson["title"],
            "url": lesson["url"],
            "type": "site",
            "authority": "Current Lesson",
            "file_id": None,
        }

        already_present = any(
            reference.get("url")
            == lesson["url"]
            for reference in references
        )

        if not already_present:

            references.insert(
                0,
                current_lesson_reference
            )


    return references

def is_navigation_request(message):
    """
    Return True only when the user explicitly asks
    the application to navigate somewhere.
    """

    text = message.lower().strip()

    phrases = [
        "jump me",
        "take me there",
        "take me to",
        "go there",
        "go to it",
        "open it",
        "open that",
        "open the lesson",
        "open the section",
        "show me that lesson",
        "show me the section",
    ]

    return any(
        phrase in text
        for phrase in phrases
    )

def should_force_library_search(message):
    """
    Force retrieval for substantive questions/searches.

    Short conversational follow-ups can use conversation
    memory without being forced to perform another search.
    """

    text = message.strip().lower()

    conversational_followups = {
        "yes",
        "yes please",
        "yeah",
        "yep",
        "no",
        "nope",
        "ok",
        "okay",
        "go",
        "continue",
        "do it",
        "explain that",
        "explain more",
        "tell me more",
        "why",
        "how",
        "what do you mean",
        "thanks",
        "thank you",
    }

    if text in conversational_followups:
        return False

    return True

def ask_aviation_assistant(
    message,
    scope,
    current_path=None,
    previous_response_id=None,
    last_site_url=None,
):
    """
    Main aviation assistant.

    scope:
        library
        lesson

    previous_response_id:
        Gives each chat conversational memory.

    last_site_url:
        Last verified SITE_CONTENT result from this
        specific conversation.
    """

    if scope not in {
        "library",
        "lesson",
    }:
        raise ValueError(
            "Invalid chat scope."
        )

    if not SITE_VECTOR_STORE_ID:
        raise RuntimeError(
            "OPENAI_SITE_VECTOR_STORE_ID is missing."
        )

    if not APPROVED_VECTOR_STORE_ID:
        raise RuntimeError(
            "OPENAI_APPROVED_VECTOR_STORE_ID is missing."
        )


    lesson = None


    # -----------------------------------------------------
    # LIBRARY CHAT
    # -----------------------------------------------------

    if scope == "library":

        vector_store_ids = [
            SITE_VECTOR_STORE_ID,
            APPROVED_VECTOR_STORE_ID,
        ]

        user_input = message

        if should_force_library_search(message):
            tool_choice = "required"
        else:
            tool_choice = "auto"


    # -----------------------------------------------------
    # CURRENT LESSON CHAT
    # -----------------------------------------------------

    else:

        lesson = get_current_lesson(
            current_path
        )

        if lesson is None:
            raise ValueError(
                "Current lesson could not be resolved."
            )

        vector_store_ids = [
            APPROVED_VECTOR_STORE_ID
        ]

        user_input = f"""
CURRENT LESSON

Title:
{lesson["title"]}

URL:
{lesson["url"]}

LESSON CONTENT
---------------
{lesson["content"]}
---------------

USER QUESTION

{message}
"""

        # The exact lesson is already supplied.
        # Approved-source retrieval remains available when needed.
        tool_choice = "auto"


    # -----------------------------------------------------
    # OPENAI REQUEST
    # -----------------------------------------------------

    request_args = {
        "model": OPENAI_CHAT_MODEL,

        "instructions": build_chat_instructions(
            scope
        ),

        "input": user_input,

        "tools": [
            {
                "type": "file_search",
                "vector_store_ids": vector_store_ids,
                "max_num_results": 10,
            }
        ],

        "tool_choice": tool_choice,

        "include": [
            "file_search_call.results"
        ],

        # Explicitly retain response state so the next
        # previous_response_id can continue the conversation.
        "store": True,
    }


    if previous_response_id:
        request_args[
            "previous_response_id"
        ] = previous_response_id


    response = openai_client.responses.create(
        **request_args
    )


    # -----------------------------------------------------
    # ACTUAL RETRIEVED SOURCES
    # -----------------------------------------------------

    sources = extract_search_sources(
        response
    )
    references = extract_response_references(
        response,
        lesson=lesson,
    )

    # Current lesson was supplied directly rather than
    # retrieved through File Search.

    if lesson is not None:

        sources.insert(
            0,
            {
                "title": lesson["title"],
                "url": lesson["url"],
                "type": "site",
                "authority": "Current Lesson",
            }
        )


    # -----------------------------------------------------
    # FIND LAST VERIFIED SITE URL
    # -----------------------------------------------------

    retrieved_site_urls = [
        source["url"]
        for source in sources
        if source.get("type") == "site"
        and source.get("url")
    ]


    verified_site_url = (
        retrieved_site_urls[0]
        if retrieved_site_urls
        else last_site_url
    )


    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    navigate_to = None

    if is_navigation_request(message):

        if verified_site_url:
            navigate_to = verified_site_url


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {
        "answer": response.output_text,

        "references": references,

        "sources": sources,

        "response_id": response.id,

        "last_site_url": verified_site_url,

        "navigate_to": navigate_to,
    }
# ---------------------------------------------------------
# CONTENT TREE
# ---------------------------------------------------------

def build_tree(path, parent_slugs=None):

    if parent_slugs is None:
        parent_slugs = []

    nodes = []

    if not path.exists():
        return nodes

    for item in sorted(path.iterdir()):

        if not item.is_dir():
            continue

        # Assets never become navigation items.
        if item.name.lower() == "assets":
            continue

        current_slugs = (
            parent_slugs
            + [slugify(item.name)]
        )

        url = "/" + "/".join(
            current_slugs
        )

        node = {
            "title": display_name(item.name),
            "url": url,
            "has_lesson": (
                item / "lesson.md"
            ).is_file(),
            "children": build_tree(
                item,
                current_slugs,
            ),
        }

        nodes.append(node)

    return nodes


# ---------------------------------------------------------
# RESOLVE URL BACK TO REAL FOLDER
# ---------------------------------------------------------

def resolve_content_folder(content_path):

    segments = [
        segment
        for segment in content_path.split("/")
        if segment
    ]

    current = CONTENT_ROOT

    for segment in segments:

        matches = []

        for item in current.iterdir():

            if not item.is_dir():
                continue

            if item.name.lower() == "assets":
                continue

            if slugify(item.name) == segment:
                matches.append(item)

        if len(matches) != 1:
            abort(404)

        current = matches[0]

    return current


# ---------------------------------------------------------
# LIBRARY / COURSE CATALOG
# ---------------------------------------------------------

SECTION_CONFIG = {
    "acs-study-guides": {
        "title": "ACS Study Guides",
        "folder": "acs_study_guides",
        "description": (
            "ACS-organized study guides built around "
            "Knowledge, Risk Management, and Skills."
        ),
    },
    "training-syllabi": {
        "title": "Training Syllabi",
        "folder": "training_syllabi",
        "description": (
            "Structured training paths organized by "
            "certificate or instructor rating."
        ),
    },
}

COURSE_CONFIG = [
    ("private", "Private"),
    ("instrument", "Instrument"),
    ("commercial", "Commercial"),
    ("cfi", "CFI"),
    ("cfii", "CFII"),
]

def course_has_content(
    section_folder,
    course_slug,
):
    """
    A course is available only when at least one
    lesson.md exists somewhere below its folder.
    """

    course_root = (
        CONTENT_ROOT
        / section_folder
        / course_slug
    )

    if not course_root.is_dir():
        return False

    return any(
        course_root.rglob(
            "lesson.md"
        )
    )

def build_home_catalog():

    catalog = []

    for section_slug, section in SECTION_CONFIG.items():

        courses = []

        for course_slug, course_title in COURSE_CONFIG:

            courses.append({
                "title": course_title,

                "url": (
                    f"/{section_slug}/{course_slug}"
                ),

                "available": course_has_content(
                    section["folder"],
                    course_slug,
                ),
            })

        catalog.append({
            "title": section["title"],
            "description": section["description"],
            "courses": courses,
        })

    return catalog


def get_course_context(content_path):
    """
    Return the course-level navigation context for paths such as:

        /acs-study-guides/cfi
        /acs-study-guides/cfi/area-i/task-a
        /training-syllabi/private/solo-qualification

    The sidebar is intentionally scoped to only the selected course.
    """

    segments = [
        segment
        for segment in content_path.split("/")
        if segment
    ]

    if len(segments) < 2:
        return None

    section_slug = segments[0]
    course_slug = segments[1]

    section = SECTION_CONFIG.get(
        section_slug
    )

    course_lookup = dict(
        COURSE_CONFIG
    )

    course_title = course_lookup.get(
        course_slug
    )

    if (
        section is None
        or course_title is None
    ):
        return None

    course_root = (
        CONTENT_ROOT
        / section["folder"]
        / course_slug
    )

    tree = build_tree(
        course_root,
        parent_slugs=[
            section_slug,
            course_slug,
        ],
    )

    return {
        "section_slug": section_slug,
        "section_title": section["title"],
        "course_slug": course_slug,
        "course_title": course_title,
        "course_root": course_root,
        "tree": tree,
        "nav_title": (
            f"{course_title} · "
            f"{section['title']}"
        ),
    }


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html",
        tree=[],
        nav_title=None,
        catalog=build_home_catalog(),
        current_path="/",
    )


# ---------------------------------------------------------
# COURSE HOME
# ---------------------------------------------------------

@app.route(
    "/<section_slug>/<course_slug>"
)
def course_home(
    section_slug,
    course_slug,
):

    content_path = (
        f"{section_slug}/{course_slug}"
    )

    context = get_course_context(
        content_path
    )

    if context is None:
        abort(404)

    return render_template(
        "course.html",
        tree=context["tree"],
        nav_title=context["nav_title"],
        section_title=context["section_title"],
        course_title=context["course_title"],
        current_path="/" + content_path,
    )


# ---------------------------------------------------------
# LESSON ASSETS
# ---------------------------------------------------------

@app.route(
    "/<path:content_path>/assets/<path:filename>"
)
def lesson_asset(
    content_path,
    filename,
):

    folder = resolve_content_folder(
        content_path
    )

    assets_folder = (
        folder / "assets"
    )

    if not assets_folder.is_dir():
        abort(404)

    return send_from_directory(
        assets_folder,
        filename,
    )


# ---------------------------------------------------------
# TRAINING LESSON SECTIONS
# ---------------------------------------------------------

TRAINING_LESSON_SECTIONS = {
    "prepare": "prepare",
    "ground brief": "brief",
    "brief": "brief",
    "flight card": "fly",
    "fly": "fly",
    "debrief": "debrief",
}


CFI_ACS_LESSON_SECTIONS = {
    "prepare": "prepare",
    "teach": "teach",
    "fly": "fly",
    "review": "review",
}


def split_training_lesson_markdown(markdown_text):
    """
    Split a training syllabus lesson into top-level sections.

    Everything before # Prepare becomes Overview.

    Recognized headings:

        # Prepare
        # Ground Brief
        # Flight Card
        # Debrief
    """

    sections = {
        "overview": [],
        "prepare": [],
        "brief": [],
        "fly": [],
        "debrief": [],
    }

    current_section = "overview"

    for line in markdown_text.splitlines(
        keepends=True
    ):

        match = re.match(
            r"^\s*#\s+(.+?)\s*$",
            line,
        )

        if match:

            heading = (
                match.group(1)
                .strip()
                .lower()
            )

            heading = re.sub(
                r"\s+",
                " ",
                heading,
            )

            mapped_section = (
                TRAINING_LESSON_SECTIONS.get(
                    heading
                )
            )

            if mapped_section:

                current_section = mapped_section

                # The tab itself supplies the title,
                # so do not retain the H1 heading.
                continue

        sections[
            current_section
        ].append(line)

    return {
        section: "".join(lines).strip()
        for section, lines in sections.items()
    }


def split_cfi_acs_lesson_markdown(markdown_text):
    """
    Split a CFI ACS lesson into the CFI-specific tab sections.

    Everything before the first recognized heading becomes Overview.
    Training Syllabus heading recognition remains isolated in
    split_training_lesson_markdown().
    """

    sections = {
        "overview": [],
        "prepare": [],
        "teach": [],
        "fly": [],
        "review": [],
    }

    current_section = "overview"

    for line in markdown_text.splitlines(
        keepends=True
    ):

        match = re.match(
            r"^\s*#\s+(.+?)\s*$",
            line,
        )

        if match:

            heading = re.sub(
                r"\s+",
                " ",
                match.group(1).strip().lower(),
            )

            mapped_section = (
                CFI_ACS_LESSON_SECTIONS.get(
                    heading
                )
            )

            if mapped_section:

                current_section = mapped_section

                # The CFI tab supplies the section title.
                continue

        sections[current_section].append(line)

    return {
        section: "".join(lines).strip()
        for section, lines in sections.items()
    }


def render_lesson_markdown(markdown_text):
    """
    Run one lesson section through the site's existing
    custom widgets and Markdown renderer.
    """

    if not markdown_text:
        return ""

    markdown_text = process_custom_embeds(
        markdown_text
    )

    lesson_html = markdown.markdown(
        markdown_text,
        extensions=[
            "extra",
            "sane_lists",
        ],
    )

    return make_markdown_links_new_tab(
        lesson_html
    )


# ---------------------------------------------------------
# LESSON PAGE
# ---------------------------------------------------------

@app.route(
    "/<path:content_path>"
)
def lesson(content_path):

    folder = resolve_content_folder(
        content_path
    )

    lesson_file = (
        folder / "lesson.md"
    )

    if not lesson_file.is_file():
        abort(404)

    markdown_text = lesson_file.read_text(
        encoding="utf-8"
    )

    is_training_lesson = (
        content_path.startswith(
            "training-syllabi/"
        )
    )

    is_cfi_acs_lesson = (
        content_path.startswith(
            "acs-study-guides/cfi/"
        )
    )

    lesson_sections = None
    lesson_html = None

    if is_training_lesson:

        raw_sections = split_training_lesson_markdown(
            markdown_text
        )

        lesson_sections = {
            section_name: render_lesson_markdown(
                section_markdown
            )
            for section_name, section_markdown
            in raw_sections.items()
        }

    elif is_cfi_acs_lesson:

        raw_sections = split_cfi_acs_lesson_markdown(
            markdown_text
        )

        lesson_sections = {
            section_name: render_lesson_markdown(
                section_markdown
            )
            for section_name, section_markdown
            in raw_sections.items()
        }

    else:

        lesson_html = render_lesson_markdown(
            markdown_text
        )

    course_context = get_course_context(
        content_path
    )

    if course_context is None:
        abort(404)

    tree = course_context["tree"]

    title = display_name(
        folder.name
    )

    area_title = display_name(
        folder.parent.name
    )

    return render_template(
        "lesson.html",
        tree=tree,
        nav_title=course_context["nav_title"],
        title=title,
        lesson_html=lesson_html,
        lesson_sections=lesson_sections,
        is_training_lesson=is_training_lesson,
        is_cfi_acs_lesson=is_cfi_acs_lesson,
        area_title=area_title,
        current_path="/" + content_path,
    )


@app.route("/knowledge-excerpt/<path:filename>")
def knowledge_excerpt(filename):
    """
    Serve a temporary PDF containing only the requested
    inclusive page range from an approved local PDF.

    Pages are 1-based for authoring convenience.
    """

    start_page = request.args.get(
        "start",
        type=int,
    )

    end_page = request.args.get(
        "end",
        type=int,
    )

    if (
        start_page is None
        or end_page is None
        or start_page < 1
        or end_page < start_page
    ):
        abort(400)

    root = KNOWLEDGE_ROOT.resolve()

    source_path = (
        KNOWLEDGE_ROOT
        / filename
    ).resolve()

    try:
        source_path.relative_to(root)
    except ValueError:
        abort(404)

    if (
        not source_path.is_file()
        or source_path.suffix.lower() != ".pdf"
    ):
        abort(404)

    source_stat = source_path.stat()

    cache_key = hashlib.sha256(
        (
            f"{source_path}|"
            f"{source_stat.st_mtime_ns}|"
            f"{source_stat.st_size}|"
            f"{start_page}|{end_page}"
        ).encode("utf-8")
    ).hexdigest()[:24]

    temp_root = (
        Path(tempfile.gettempdir())
        / "cfi_syllabus_pdf_excerpts"
    )

    temp_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    excerpt_path = (
        temp_root
        / (
            f"{source_path.stem}_"
            f"pages_{start_page}-{end_page}_"
            f"{cache_key}.pdf"
        )
    )

    if excerpt_path.exists():
        return send_file(
            excerpt_path,
            mimetype="application/pdf",
            as_attachment=False,
            conditional=True,
        )

    reader = PdfReader(
        str(source_path)
    )

    page_count = len(reader.pages)

    if end_page > page_count:
        abort(400)

    if not excerpt_path.exists():

        writer = PdfWriter()

        for page_index in range(
            start_page - 1,
            end_page,
        ):
            writer.add_page(
                reader.pages[page_index]
            )

        with excerpt_path.open("wb") as output:
            writer.write(output)

    return send_file(
        excerpt_path,
        mimetype="application/pdf",
        as_attachment=False,
        conditional=True,
    )


@app.route("/knowledge/<path:filename>")
def knowledge_file(filename):

    return send_from_directory(
        KNOWLEDGE_ROOT,
        filename
    )

@app.route(
    "/api/chat",
    methods=["POST"]
)
def api_chat():

    data = request.get_json(
        silent=True
    ) or {}


    message = str(
        data.get("message", "")
    ).strip()


    scope = str(
        data.get("scope", "library")
    ).strip().lower()


    current_path = data.get(
        "current_path"
    )


    previous_response_id = data.get(
        "previous_response_id"
    )


    last_site_url = data.get(
        "last_site_url"
    )


    if not message:

        return jsonify({
            "error": "Message is required."
        }), 400


    try:

        result = ask_aviation_assistant(
            message=message,
            scope=scope,
            current_path=current_path,
            previous_response_id=previous_response_id,
            last_site_url=last_site_url,
        )

        return jsonify(
            result
        )


    except ValueError as exc:

        return jsonify({
            "error": str(exc)
        }), 400


    except Exception:

        app.logger.exception(
            "Chat request failed."
        )

        return jsonify({
            "error":
                "The aviation assistant request failed."
        }), 500
# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )