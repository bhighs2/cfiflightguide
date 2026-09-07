# Flight Guide Lesson Authoring Reference

Flight Guide uses separate authoring standards depending on the content type.

The detailed authoring documents carry the process. Normal Copilot prompts should stay short and route the work to the correct standard.

---

# 1. Training Syllabi

For sequential training syllabus lessons under:

`content/training_syllabi/`

use these files together.

## `FLIGHT_GUIDE_LESSON_BUILD_PROTOCOL.md`

Permanent rules for how Flight Guide Training Syllabus lessons are researched, aligned, structured, generated, and quality-checked.

This is the main authoring standard for sequential student-training lessons.

## `FLIGHT_GUIDE_SOURCE_ALIGNMENT_WORKSHEET.md`

Use this for every new Training Syllabus lesson.

Complete the worksheet collaboratively **before** generating the final `lesson.md`.

The key rule is the **Source Alignment Gate**: do not jump directly from a lesson title to a finished lesson.

First align on:

- scope,
- adjacent-lesson ownership,
- course continuity,
- regulations / ACS,
- PDFs,
- images,
- videos,
- mnemonics,
- highlights,
- risks,
- procedures,
- common errors,
- scenarios,
- Fly-section planning,
- kneeboard items.

## `FLIGHT_GUIDE_LESSON_TEMPLATE.md`

Canonical copy-ready `lesson.md` structure for Training Syllabus lessons.

Use it only after the source-alignment worksheet is approved.

Training Syllabus lessons use the established Flight Guide architecture:

**Overview | Prepare | Brief | Fly | Debrief**

Not every lesson requires every tab.

---

# 2. CFI ACS Lesson Plans

For CFI ACS Area/Task lessons under:

`content/acs_study_guides/cfi/`

use:

## `CFI_ACS_LESSON_AUTHORING_PROTOCOL.md`

This is the permanent authoring standard for CFI ACS lesson plans.

CFI ACS lessons are organized exactly by the current CFI ACS Area and Task and are designed to serve two purposes:

1. An interactive CFI study and teaching reference in Flight Guide.
2. A clean, printable CFI lesson-plan reference.

CFI ACS lessons use:

**Overview | Prepare | Teach | Fly | Review**

`Fly` is conditional and appears only when the Task contains meaningful flight or maneuver instruction.

For CFI ACS work, the CFI ACS Lesson Authoring Protocol takes precedence over the Training Syllabus Build Protocol, Source Alignment Worksheet, and Lesson Template when the instructions differ.

The CFI ACS protocol establishes:

- current ACS verification,
- Binns Flight Services as the structural and coverage baseline,
- exact ACS Knowledge / Risk Management / Skills mapping,
- FAA source verification,
- Prepare as the deeper-study area,
- Teach as the concise printable teaching section,
- Fly structure for maneuver Tasks,
- common-error recognition and correction,
- inline screenshots and diagrams,
- video timing rules,
- vertical-rail Kneeboard structure,
- Review questions and answers,
- printable-lesson requirements.

Do not apply the CFI lesson-plan architecture to Private, Instrument, or Commercial ACS study guides unless specifically instructed.

---

# 3. Recommended Training Syllabus Workflow

For every new Training Syllabus lesson:

1. State the lesson number and title.
2. Open the Source Alignment Worksheet.
3. Establish scope and boundaries.
4. Build the Course Continuity map: **Builds On → Current Lesson → Leads To**.
5. Align FAA / ACS / regulatory requirements.
6. Review PDF sources and exact page ranges.
7. Suggest and approve useful images.
8. Suggest and approve useful videos.
9. Identify mnemonics and memory aids.
10. Identify attention / safety / highlight items.
11. Identify Risk Management topics.
12. Identify skills and procedures.
13. Pull all available FAA / source Common Errors.
14. Develop scenario applications.
15. Plan the Fly section.
16. Plan the abbreviated kneeboard.
17. Mark the worksheet **READY TO GENERATE**.
18. Generate the complete `lesson.md`.
19. Run the Build Protocol QA checklist.

This preserves the workflow:

**ALIGN FIRST → BUILD SECOND → QA THIRD**

---

# 4. Recommended CFI ACS Workflow

For every new CFI ACS lesson:

1. Identify the exact current ACS Area and Task.
2. Verify the current ACS Objective and every K / R / S element.
3. Review the matching Binns Flight Services lesson.
4. Inspect the approved FAA source material in the repo.
5. Review the latest approved CFI ACS lesson for house style.
6. Incorporate user-provided images, videos, common errors, techniques, and references.
7. Resolve any differences in favor of the current ACS and controlling FAA source.
8. Build the complete `lesson.md` using the CFI ACS Lesson Authoring Protocol.
9. Run the CFI ACS protocol quality-control checklist.

If the user requests source alignment before generation, do not generate the final `lesson.md` until the user approves the alignment.

The initial CFI ACS house-style reference is:

**Area VIII, Task A — Straight-and-Level Flight**

---

# 5. Minimal Agent Invocation

Once these files are in the repo and referenced by Copilot instructions, normal lesson-development prompts should be short.

## Training Syllabus example

```text
Work on Private Lesson 2 — Airport Environment, Communications and Surface Operations.

Follow the Flight Guide lesson-authoring docs. Start with source alignment and do not generate the final lesson.md until I approve it.
```

## CFI ACS example

```text
Work on CFI ACS Area VIII, Task A — Straight-and-Level Flight.

Follow the CFI ACS Lesson Authoring Protocol. Review the current ACS Task, the matching Binns lesson, approved FAA sources, and the latest approved CFI ACS lesson for house style. Incorporate the user-provided images/videos/references exactly where relevant and build the complete lesson.md.
```

The authoring documents—not the prompt—should carry the detailed process.

## Flight Guide Knowledge-Base Rule

All future lesson factual content must come only from the Flight Guide knowledge base. Authors must inspect the local approved source material or indexed source text before writing each section. Do not create factual explanations, examples, procedures, common errors, scenarios, review answers, or completion standards from general knowledge or external material.

External websites, Binns, videos, and user-provided material may guide lesson structure or be listed as supplemental references, but they cannot be used as the factual source unless they have been incorporated into the Flight Guide knowledge base first.

Concise synthesis of key knowledge-base information is encouraged when it improves instruction. Flight Guide instructor principles, mnemonics, memory aids, and highlights may draw on Flight Guide or explicitly user-provided instructional material, provided they are labeled as Flight Guide material when they are not FAA-defined language and are not represented as controlling FAA fact.

---

# 6. Permanent Source-Alignment Guardrails

These rules apply across Flight Guide lesson authoring.

## PDF page numbers

**Never guess PDF embed page numbers.**

`start=` / `end=` values are added only after the actual physical PDF page positions are verified against the real source file.

Search-index, extracted-text, printed-book, table-of-contents, or inferred page numbers are not sufficient by themselves.

If the physical page mapping is not verified, embed the full PDF or leave the page range unassigned.

A user-confirmed physical PDF range is authoritative.

## Source presence

Before stating that an approved source is missing, inspect the actual filenames in `knowledge/approved/`.

Do not treat absence from a semantic index, text index, extracted-text cache, or search result as proof that the file is not present.

## Videos

Always consider video deliberately.

The absence of an approved video in the repo is not a reason to skip the category.

When search is available, propose actual candidates.

When search is not available, propose specific search targets.

Keep video status unresolved until the user approves a video or explicitly chooses none.

Do not guess timestamps.

If the user provides chapter timestamps, use the smallest relevant continuous cut for the lesson or Task.

## Images

Use images, screenshots, diagrams, tables, and figures when they materially improve understanding.

Do not use decorative imagery that adds no instructional value.

Use user-provided filenames exactly.

## Aircraft-specific information

Do not invent aircraft-specific:

- airspeeds,
- power settings,
- capacities,
- limitations,
- configurations,
- procedures.

Verify exact aircraft-specific information against the applicable POH / AFM / checklist.

---

# 7. Training Syllabus Fly and Kneeboard House Style

For every new **GROUND + FLIGHT** Training Syllabus lesson:

- Do not stop the Fly section at surface operations.
- Include either **Air Work** or **Air Work Reinforcement**.
- If there is no new airborne maneuver, deliberately repeat prior lesson airwork with a progression target.
- Use the approved HTML vertical-rail kneeboard architecture from the most recently approved lesson.
- Do not regress to plain Markdown kneeboard headings or bullets.
- Include an `AIR WORK` kneeboard rail when airborne work is part of the lesson.
- Add lesson-specific rails such as `SURFACE` or `RADIO` when they improve operational usefulness.
- Local radio-call examples must use user-confirmed airport, callsign, ramp, runway, taxi route, and related details.

---

# 8. CFI ACS Printable-Lesson House Style

CFI ACS lessons are authored so the same `lesson.md` works both on screen and as a hard-copy lesson reference.

The primary printable lesson contains:

1. **Overview**
2. **Teach**
3. **Fly**, when applicable
4. **Kneeboard**, when applicable

The primary printable lesson excludes:

- Prepare,
- Review,
- videos,
- embedded PDF viewers,
- site navigation,
- tabs / buttons,
- other web-only controls.

The Kneeboard is the final H2 section inside Fly and is appended at the end of the printable CFI lesson.

When printed, the Kneeboard begins on a new page.

The same `lesson.md` drives both web and print. Do not create a second printable Markdown file.

---

# 9. Permanent Product Distinction

Do not blur these Flight Guide products.

## Training Syllabi

Sequential real-student training lesson plans organized by instructional progression.

## CFI ACS

ACS-organized lesson plans designed for CFI oral / practical preparation and teaching demonstration.

## Private / Instrument / Commercial ACS

ACS-organized study guides unless another format is explicitly established.

The same aviation subject may appear in more than one product for a different purpose. That is intentional.
