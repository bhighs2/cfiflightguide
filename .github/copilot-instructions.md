## Flight Guide Lesson Authoring

When creating or modifying training syllabus lesson files, first read:

- `docs/lesson_authoring/FLIGHT_GUIDE_LESSON_BUILD_PROTOCOL.md`
- `docs/lesson_authoring/FLIGHT_GUIDE_SOURCE_ALIGNMENT_WORKSHEET.md`
- `docs/lesson_authoring/FLIGHT_GUIDE_LESSON_TEMPLATE.md`

For new lessons, do not immediately generate the final `lesson.md`.

Follow this workflow:

1. Establish lesson scope and adjacent-lesson boundaries.
2. Align regulatory and ACS requirements.
3. Align PDF/document sources and exact page ranges.
4. Suggest useful images, diagrams, videos, mnemonics, memory aids, and highlight items.
5. Identify Risk Management topics.
6. Identify procedures and all available FAA/source Common Errors.
7. Develop scenario applications.
8. Plan the abbreviated kneeboard.
9. Confirm the source-alignment gate is complete.
10. Only then generate the final `lesson.md`.

Preserve the existing Flight Guide Markdown syntax and lesson architecture.

## Markdown List Nesting

**HARD, always:** Indent every sub-bullet with **four spaces for each nesting level**. Never use two-space indentation for child bullets; the Flight Guide Markdown renderer treats two-space bullets as top-level siblings. After editing nested lists, verify that child bullets render as nested `<ul>` elements rather than flat sibling `<li>` elements.

## CFI ACS Lesson Authoring

When creating or modifying CFI ACS lesson files under:

- `content/acs_study_guides/cfi/`

first read:

- `docs/lesson_authoring/CFI_ACS_LESSON_AUTHORING_PROTOCOL.md`

All factual lesson content must be sourced only from the Flight Guide knowledge base. Inspect the relevant approved local source or indexed source text before drafting. Do not use general knowledge, Binns, external websites, videos, or user-provided material as the factual source unless it has first been added to the Flight Guide knowledge base. Keep or incorporate user-provided assets, links, clips, videos, and other explicitly requested resources as supplemental lesson material.

Synthesize key knowledge-base information into concise teaching material when useful. Flight Guide instructor principles, mnemonics, memory aids, and highlights may use Flight Guide or explicitly user-provided instructional material; label them as Flight Guide material when they are not FAA-defined language, and do not present them as controlling FAA fact.

The CFI ACS lesson-authoring protocol governs these files and takes precedence over the Training Syllabus authoring instructions when the two differ.

CFI ACS lessons are standalone lesson plans organized exactly by CFI ACS Area and Task.

Use the established Flight Guide CFI architecture:

- Overview
- Prepare
- Teach
- Fly — only when applicable
- Review

Use Binns Flight Services https://binnsflightservices.com/lessonplans as the baseline for lesson organization, simplicity, topic flow, and content coverage, while verifying against the current FAA CFI ACS and approved FAA source material.

Preserve useful Flight Guide enhancements without cluttering the core lesson:

- exact ACS Knowledge, Risk Management, and Skills elements
- FAA source references
- screenshots and diagrams placed directly with the applicable Teach content
- videos and deeper source material primarily in Prepare
- mnemonics and highlights where useful
- aviation-specific examples
- common errors and instructor corrections

### Scanability Rule

**HARD, always:** Bold section labels, procedure names, decision triggers, limitations, speeds, configuration items, risk cues, common-error names, and other high-value technical phrases throughout the lesson so the page is quickly scannable in print and on screen. Do not bold entire paragraphs or routine connective prose; emphasis must identify the information the instructor or learner needs to find quickly.

For flight Tasks:

- include a complete Fly section
- place `## Kneeboard` as the final H2 section of Fly
- use the established compact vertical-rail kneeboard architecture

CFI lesson print output is designed to use:

- Overview
- Teach
- Fly, when applicable
- Kneeboard, when applicable

Prepare and Review are supplemental web-study sections and are not part of the primary printed lesson.

Do not apply the CFI lesson-plan architecture to Private, Instrument, or Commercial ACS study guides unless specifically instructed.