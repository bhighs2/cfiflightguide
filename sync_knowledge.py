from pathlib import Path
from datetime import datetime, timezone
import hashlib
import os
import re
import sqlite3

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

CONTENT_ROOT = Path("content")
APPROVED_ROOT = Path("knowledge/approved")
INDEX_ROOT = Path("knowledge/index")
DB_PATH = "knowledge_manifest.db"

SITE_VECTOR_STORE_ID = os.getenv(
    "OPENAI_SITE_VECTOR_STORE_ID"
)

APPROVED_VECTOR_STORE_ID = os.getenv(
    "OPENAI_APPROVED_VECTOR_STORE_ID"
)

client = OpenAI(
    max_retries=5,
)


# ---------------------------------------------------------
# BASIC UTILITIES
# ---------------------------------------------------------

def file_hash(path):
    sha256 = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def clean_name(name):
    """
    01_Solo_Qualification
    becomes:
    Solo Qualification
    """

    if "_" in name and name.split("_", 1)[0].isdigit():
        name = name.split("_", 1)[1]

    return name.replace("_", " ")


def slugify(name):
    text = clean_name(name).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)

    return text.strip("-")


def now_utc():
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------
# SITE CONTENT
# ---------------------------------------------------------

def site_canonical_url(lesson):
    relative = lesson.parent.relative_to(CONTENT_ROOT)

    parts = [
        slugify(part)
        for part in relative.parts
    ]

    return "/" + "/".join(parts)


def site_attributes(lesson):
    relative = lesson.parent.relative_to(CONTENT_ROOT)

    raw_parts = relative.parts

    cleaned_parts = [
        clean_name(part)
        for part in raw_parts
    ]

    return {
        "source_type": "site",
        "course": cleaned_parts[0].lower(),
        "title": cleaned_parts[-1],
        "hierarchy": " > ".join(cleaned_parts)[:512],
        "canonical_url": site_canonical_url(lesson),
    }


def scan_site_content():

    lessons = []

    for path in CONTENT_ROOT.rglob("lesson.md"):

        # Never treat something inside assets as a page.
        if "assets" in [
            part.lower()
            for part in path.parts
        ]:
            continue


        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        lines = text.splitlines()

        objective_lines = []
        inside_objective = False


        for line in lines:

            stripped = line.strip()


            # Start of Objective section.
            if stripped == "## Objective":

                inside_objective = True
                continue


            # Stop when the next level-2 heading begins.
            if (
                inside_objective
                and stripped.startswith("## ")
            ):

                break


            if inside_objective:

                objective_lines.append(
                    line
                )


        objective_text = "\n".join(
            objective_lines
        ).strip()


        # No Objective content = blank template.
        if not objective_text:

            print(
                "SKIPPED TEMPLATE: "
                + path.relative_to(
                    CONTENT_ROOT
                ).as_posix()
            )

            continue


        lessons.append(
            path
        )


    return sorted(
        lessons
    )


# ---------------------------------------------------------
# APPROVED AVIATION SOURCES
# ---------------------------------------------------------

def build_approved_page_index(pdf_path):
    """
    Build a local page-aware text representation of an
    approved PDF.

    The original PDF remains the file sent to OpenAI.

    This text file is used only by the Flask application
    to map retrieved passages back to physical PDF pages.
    """

    pdf_path = Path(pdf_path)

    relative = pdf_path.relative_to(
        APPROVED_ROOT
    )

    output_path = (
        INDEX_ROOT
        / relative.parent
        / f"{relative.name}.txt"
    )

    # Do not rebuild if the index already exists and is
    # at least as new as the source PDF.
    if (
        output_path.exists()
        and output_path.stat().st_mtime
        >= pdf_path.stat().st_mtime
    ):
        print(
            f"PAGE INDEX UNCHANGED: {relative.as_posix()}"
        )

        return output_path

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    reader = PdfReader(
        str(pdf_path)
    )

    print(
        f"BUILDING PAGE INDEX: {relative.as_posix()}"
    )

    print(
        f"  Pages: {len(reader.pages)}"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as output:

        output.write(
            f"DOCUMENT_TITLE: {pdf_path.stem}\n"
        )

        output.write(
            f"SOURCE_FILE: {relative.as_posix()}\n"
        )

        output.write(
            "SOURCE_TYPE: authoritative\n"
        )

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            try:
                text = (
                    page.extract_text()
                    or ""
                )

            except Exception as exc:

                print(
                    f"  WARNING: "
                    f"page {page_number}: {exc}"
                )

                text = ""

            output.write("\n\n")
            output.write(
                "========================================\n"
            )

            output.write(
                f"<<<PDF_PAGE:{page_number}>>>\n"
            )

            output.write(
                f"<<<SOURCE_FILE:"
                f"{relative.as_posix()}>>>\n"
            )

            output.write(
                "========================================\n\n"
            )

            output.write(
                text.strip()
            )

            output.write("\n")

    print(
        f"  Created: {output_path}"
    )

    return output_path

def approved_attributes(path):
    relative = path.relative_to(APPROVED_ROOT)

    title = path.stem.replace("_", " ")

    return {
        "source_type": "authoritative",
        "authority": "FAA",
        "title": title,
        "source_path": relative.as_posix()[:512],
    }


def scan_approved_sources():
    """
    For now we are intentionally limiting the authoritative
    knowledge base to PDF files.
    """

    return sorted(
        APPROVED_ROOT.rglob("*.pdf")
    )


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            content_hash TEXT NOT NULL,
            openai_file_id TEXT,
            canonical_url TEXT,
            last_indexed TEXT
        )
    """)

    conn.commit()

    migrate_existing_manifest(conn)

    return conn


def migrate_existing_manifest(conn):
    """
    Older manifest rows were created before we had two
    knowledge bases.

    Those rows are existing SITE_CONTENT records.

    Convert:

    private\\01_Solo...\\lesson.md

    to:

    site:private/01_Solo.../lesson.md
    """

    rows = conn.execute("""
        SELECT path
        FROM files
    """).fetchall()

    for row in rows:
        old_path = row[0]

        if old_path.startswith("site:"):
            continue

        if old_path.startswith("approved:"):
            continue

        normalized = old_path.replace("\\", "/")

        new_path = "site:" + normalized

        conn.execute("""
            UPDATE files
            SET path = ?
            WHERE path = ?
        """, (
            new_path,
            old_path
        ))

    conn.commit()


# ---------------------------------------------------------
# OPENAI VECTOR STORE UTILITIES
# ---------------------------------------------------------

def upload_and_index(
    local_path,
    vector_store_id,
    attributes
):
    with local_path.open("rb") as f:

        uploaded = client.files.create(
            file=f,
            purpose="assistants"
        )

    indexed = client.vector_stores.files.create_and_poll(
        vector_store_id=vector_store_id,
        file_id=uploaded.id,
        attributes=attributes
    )

    if indexed.status != "completed":
        raise RuntimeError(
            f"Indexing failed for {local_path}: "
            f"{indexed.status}"
        )

    return uploaded.id


def remove_openai_file(
    vector_store_id,
    file_id
):

    if not file_id:
        return True

    try:

        # Deleting the OpenAI File also removes it
        # from any vector stores that contain it.
        client.files.delete(
            file_id
        )

        print(
            f"  OpenAI file deleted: {file_id}"
        )

        return True


    except Exception as exc:

        print()
        print(
            f"  WARNING: OpenAI could not delete {file_id}"
        )

        print(
            f"  {type(exc).__name__}: {exc}"
        )

        print(
            "  The sync will continue and retry this "
            "deletion next time."
        )

        print()

        return False


def list_vector_store_files(vector_store_id):
    """
    Handles pagination so this continues working once
    you have more than 100 indexed files.
    """

    results = []

    page = client.vector_stores.files.list(
        vector_store_id=vector_store_id,
        limit=100
    )

    results.extend(page.data)

    while page.has_more:

        page = client.vector_stores.files.list(
            vector_store_id=vector_store_id,
            limit=100,
            after=page.last_id
        )

        results.extend(page.data)

    return results


# ---------------------------------------------------------
# ADOPT EXISTING REMOTE FILES
# ---------------------------------------------------------

def find_existing_site_file(canonical_url):
    files = list_vector_store_files(
        SITE_VECTOR_STORE_ID
    )

    for item in files:

        attributes = item.attributes or {}

        if (
            attributes.get("canonical_url")
            == canonical_url
        ):
            return item.id

    return None


def find_existing_approved_file(local_path):
    files = list_vector_store_files(
        APPROVED_VECTOR_STORE_ID
    )

    relative = local_path.relative_to(
        APPROVED_ROOT
    ).as_posix()

    title = local_path.stem.replace("_", " ")

    # First try exact source_path
    for item in files:

        attributes = item.attributes or {}

        if attributes.get("source_path") == relative:
            return item.id

    # This handles the FAA PDF we manually uploaded earlier,
    # before source_path metadata existed.
    for item in files:

        attributes = item.attributes or {}

        if (
            attributes.get("source_type")
            == "authoritative"
            and
            attributes.get("title")
            == title
        ):
            return item.id

    return None


# ---------------------------------------------------------
# SYNC ONE FILE
# ---------------------------------------------------------

def sync_file(
    conn,
    manifest_key,
    local_path,
    vector_store_id,
    attributes,
    canonical_url=None,
    existing_remote_id=None
):
    current_hash = file_hash(local_path)

    existing = conn.execute("""
        SELECT
            content_hash,
            openai_file_id
        FROM files
        WHERE path = ?
    """, (
        manifest_key,
    )).fetchone()

    # -----------------------------------------------------
    # NEW LOCAL FILE
    # -----------------------------------------------------

    if existing is None:

        # File may already exist remotely because it was
        # manually uploaded before the manifest tracked it.
        if existing_remote_id:

            print(
                f"ADOPTED: {manifest_key}"
            )

            conn.execute("""
                INSERT INTO files (
                    path,
                    content_hash,
                    openai_file_id,
                    canonical_url,
                    last_indexed
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                manifest_key,
                current_hash,
                existing_remote_id,
                canonical_url,
                now_utc()
            ))

            conn.commit()

            return

        print(
            f"NEW: {manifest_key}"
        )

        new_file_id = upload_and_index(
            local_path,
            vector_store_id,
            attributes
        )

        conn.execute("""
            INSERT INTO files (
                path,
                content_hash,
                openai_file_id,
                canonical_url,
                last_indexed
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            manifest_key,
            current_hash,
            new_file_id,
            canonical_url,
            now_utc()
        ))

        conn.commit()

        print(
            f"  Indexed: {new_file_id}"
        )

        return

    # -----------------------------------------------------
    # CHANGED LOCAL FILE
    # -----------------------------------------------------

    old_hash = existing[0]
    old_file_id = existing[1]

    if old_hash != current_hash:

        print(
            f"CHANGED: {manifest_key}"
        )

        # Upload/index replacement FIRST.
        new_file_id = upload_and_index(
            local_path,
            vector_store_id,
            attributes
        )

        # Only remove old version after successful indexing.
        if old_file_id:

            remove_openai_file(
                vector_store_id,
                old_file_id
            )

        conn.execute("""
            UPDATE files
            SET
                content_hash = ?,
                openai_file_id = ?,
                canonical_url = ?,
                last_indexed = ?
            WHERE path = ?
        """, (
            current_hash,
            new_file_id,
            canonical_url,
            now_utc(),
            manifest_key
        ))

        conn.commit()

        print(
            f"  Re-indexed: {new_file_id}"
        )

        return

    # -----------------------------------------------------
    # UNCHANGED
    # -----------------------------------------------------

    print(
        f"UNCHANGED: {manifest_key}"
    )


# ---------------------------------------------------------
# DELETE FILES NO LONGER PRESENT LOCALLY
# ---------------------------------------------------------

def remove_deleted_files(
    conn,
    prefix,
    current_keys,
    vector_store_id
):

    rows = conn.execute("""
        SELECT
            path,
            openai_file_id
        FROM files
        WHERE path LIKE ?
    """, (
        prefix + "%",
    )).fetchall()


    for manifest_key, openai_file_id in rows:

        if manifest_key in current_keys:
            continue


        print(
            f"DELETED: {manifest_key}"
        )


        # -------------------------------------------------
        # DELETE FROM OPENAI
        # -------------------------------------------------
        #
        # If OpenAI temporarily returns a 500, DO NOT
        # remove the manifest record. Keeping the record
        # allows the next sync to retry the deletion.
        # -------------------------------------------------

        if openai_file_id:

            deleted = remove_openai_file(
                vector_store_id,
                openai_file_id
            )

            if not deleted:

                print(
                    "  DELETE DEFERRED"
                )

                continue


        # -------------------------------------------------
        # DELETE LOCAL MANIFEST RECORD
        # -------------------------------------------------

        conn.execute("""
            DELETE FROM files
            WHERE path = ?
        """, (
            manifest_key,
        ))

        conn.commit()

        print(
            "  Manifest record removed"
        )


# ---------------------------------------------------------
# SITE SYNC
# ---------------------------------------------------------

def sync_site_content(conn):

    print()
    print("=" * 60)
    print("SITE CONTENT")
    print("=" * 60)

    lessons = scan_site_content()

    current_keys = set()

    for lesson in lessons:

        relative = lesson.relative_to(
            CONTENT_ROOT
        ).as_posix()

        manifest_key = (
            "site:" + relative
        )

        current_keys.add(
            manifest_key
        )

        url = site_canonical_url(
            lesson
        )

        remote_id = None

        existing = conn.execute("""
            SELECT openai_file_id
            FROM files
            WHERE path = ?
        """, (
            manifest_key,
        )).fetchone()

        if existing is None:

            remote_id = find_existing_site_file(
                url
            )

        sync_file(
            conn=conn,
            manifest_key=manifest_key,
            local_path=lesson,
            vector_store_id=SITE_VECTOR_STORE_ID,
            attributes=site_attributes(lesson),
            canonical_url=url,
            existing_remote_id=remote_id
        )

    remove_deleted_files(
        conn=conn,
        prefix="site:",
        current_keys=current_keys,
        vector_store_id=SITE_VECTOR_STORE_ID
    )

    print()
    print(
        f"Site lessons: {len(lessons)}"
    )


# ---------------------------------------------------------
# APPROVED SOURCE SYNC
# ---------------------------------------------------------

def sync_approved_sources(conn):

    print()
    print("=" * 60)
    print("APPROVED AVIATION SOURCES")
    print("=" * 60)

    sources = scan_approved_sources()

    current_keys = set()

    for source in sources:

        # Build/update the local page-aware lookup file.
        # This is NOT uploaded to OpenAI.
        build_approved_page_index(
            source
        )

        relative = source.relative_to(
            APPROVED_ROOT
        ).as_posix()

        manifest_key = (
            "approved:" + relative
        )

        current_keys.add(
            manifest_key
        )

        remote_id = None

        existing = conn.execute("""
            SELECT openai_file_id
            FROM files
            WHERE path = ?
        """, (
            manifest_key,
        )).fetchone()

        if existing is None:

            remote_id = (
                find_existing_approved_file(
                    source
                )
            )

        sync_file(
            conn=conn,
            manifest_key=manifest_key,
            local_path=source,
            vector_store_id=APPROVED_VECTOR_STORE_ID,
            attributes=approved_attributes(source),
            canonical_url=None,
            existing_remote_id=remote_id
        )

    remove_deleted_files(
        conn=conn,
        prefix="approved:",
        current_keys=current_keys,
        vector_store_id=APPROVED_VECTOR_STORE_ID
    )

    print()
    print(
        f"Approved sources: {len(sources)}"
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    if not SITE_VECTOR_STORE_ID:
        raise RuntimeError(
            "OPENAI_SITE_VECTOR_STORE_ID is missing."
        )

    if not APPROVED_VECTOR_STORE_ID:
        raise RuntimeError(
            "OPENAI_APPROVED_VECTOR_STORE_ID is missing."
        )

    conn = init_db()

    try:

        sync_site_content(conn)

        sync_approved_sources(conn)

    finally:

        conn.close()

    print()
    print("=" * 60)
    print("KNOWLEDGE SYNC COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()