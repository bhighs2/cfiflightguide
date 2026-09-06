# Flight Guide — CFI ACS Lesson Authoring Protocol

## Purpose

This document defines the permanent authoring standard for **CFI Airplane ACS lessons** in Flight Guide.

These pages serve two purposes at the same time:

1. An interactive CFI study and teaching reference on the Flight Guide website.
2. A clean, printable CFI lesson-plan reference similar in simplicity and usefulness to the Binns Flight Services CFI lesson plans.

This protocol applies to the **CFI ACS** content tree only.

Do not use this structure for the sequential Training Syllabi. Do not assume that Private, Instrument, or Commercial ACS study guides should be written as CFI lesson plans.

---

# 1. Core Authoring Philosophy

## Binns is the structural and coverage baseline

For each CFI ACS Area and Task:

1. Review the matching current CFI ACS Task.
2. Review the corresponding Binns Flight Services lesson.
3. Use the Binns lesson as the baseline for:
   - overall lesson organization,
   - teaching sequence,
   - subject coverage,
   - level of detail,
   - common-error coverage,
   - practical teaching emphasis,
   - simple, binder-friendly presentation.
4. Improve or modify the content when:
   - the current FAA ACS is more exact,
   - FAA source material has changed,
   - Binns content is incomplete or imprecise,
   - a clearer aviation example is available,
   - an aircraft-specific example improves practical usefulness,
   - the user provides a preferred teaching technique, image, video, mnemonic, or reference.

Binns is **not the controlling authority**. The current FAA ACS and current FAA source material control when there is a conflict.

Do not reproduce substantial Binns prose verbatim. Preserve the structure, factual substance, topic sequence, and instructional coverage while writing the Flight Guide version in original wording.

Binns reference:

`https://binnsflightservices.com/lessonplans`

---

# 2. Source Priority

Use this priority when building or verifying a lesson:

1. **Current FAA CFI Airplane ACS**
2. **FAA source documents named by the ACS Task**
3. **Aircraft POH/AFM when aircraft-specific information is relevant**
4. **Binns lesson for structure, coverage, and practical teaching flow**
5. **User-provided references, screenshots, videos, techniques, and local examples**
6. Other reliable aviation sources only when they materially improve the lesson

Never allow a secondary source to override the ACS or an applicable FAA/aircraft source.

---

# 3. Required Source-Alignment Workflow

Before writing or rebuilding a CFI ACS `lesson.md`:

## Step 1 — Identify the exact ACS Task

Confirm:

- Area of Operation
- Task letter
- exact Task title
- ACS references
- Objective
- every Knowledge element
- every Risk Management element
- every Skill element

Use the **exact current ACS identifiers** such as:

`AI.VIII.A.K1`

Do not invent, infer, shorten, or reuse identifiers from an older ACS.

## Step 2 — Review the matching Binns lesson

Identify:

- front-matter structure,
- lesson outline,
- teaching order,
- major explanations,
- procedures,
- common errors,
- completion standards,
- useful examples or teaching techniques.

The goal is to understand what the Binns lesson covers before drafting the Flight Guide version.

## Step 3 — Inspect approved Flight Guide sources

Inspect the actual files available under the approved knowledge source directory before stating that a source is missing.

Do not infer file absence from an index or search result alone.

Use actual approved filenames in lesson links.

Examples include:

- `/knowledge/CFI_ASEL_ACS.pdf`
- `/knowledge/Aviation_Instructors_Handbook.pdf`
- `/knowledge/Airplane_Flying_Handbook.pdf`
- `/knowledge/Pilots_Handbook_of_Aeronautical_Knowledge.pdf`
- `/knowledge/Risk_Management_Handbook.pdf`
- `/knowledge/POH-Cessna-172S.pdf`

## Step 4 — Incorporate user-provided material

If the user provides:

- image filenames,
- screenshots,
- videos,
- timestamps,
- common-error lists,
- local procedures,
- aircraft-specific techniques,
- mnemonics,
- instructor techniques,

use them as supplied unless they conflict with a controlling source.

Do not silently rename user-provided files.

Do not invent screenshots or image filenames.

## Step 5 — Resolve discrepancies

When Binns, an older lesson, and the current ACS differ:

- follow the current ACS,
- verify against the applicable FAA source,
- preserve useful Binns teaching material when still valid,
- make the Flight Guide wording more exact.

---

# 4. One File Per ACS Task

Each Task uses one file:

`lesson.md`

Do not split Overview, Prepare, Teach, Fly, or Review into separate files.

The existing Area/Task folder structure is authoritative. Do not create a new hierarchy.

---

# 5. Permanent CFI ACS Tab Architecture

CFI ACS lessons use:

**Overview | Prepare | Teach | Fly | Review**

`Fly` is conditional and appears only when the Task contains meaningful flight or maneuver instruction.

Ground-only Tasks use:

**Overview | Prepare | Teach | Review**

## Markdown boundaries

- Content before `# Prepare` = **Overview**
- `# Prepare` = **Prepare**
- `# Teach` = **Teach**
- `# Fly` = **Fly**
- `# Review` = **Review**

Do not add top-level headings that accidentally create or interfere with these panels.

---

# 6. Overview — Required Structure

The Overview is the concise Binns-style lesson-plan front matter.

Use this order unless a Task genuinely requires a small adjustment:

```markdown
# Task A. Exact ACS Task Title

**Area VIII — Exact Area Title**

## Objective

## Purpose

## Schedule / Equipment

## Learner Actions / Instructor Actions

## Completion Standards

## ACS Elements

### Knowledge

### Risk Management

### Skills

## Ground Lesson Outline
```

For a flight Task, `Ground Lesson Outline` may be named `Ground / Flight Lesson Outline` when that is clearer.

## Objective

Base the Objective on the current ACS Objective. Keep it concise and usable.

## Purpose

Explain why the subject matters operationally and instructionally. Usually one or two concise paragraphs.

## Schedule / Equipment

Include practical suggested timing and teaching equipment when useful.

Do not treat suggested lesson times as FAA requirements.

## Learner Actions / Instructor Actions

Keep this compact and action-oriented.

## Completion Standards

State what successful understanding/performance looks like.

For flight Tasks, reflect the CFI requirement to demonstrate while providing effective instruction and to meet the applicable pilot performance standard.

## ACS Elements

List **every current K/R/S element exactly**.

Example:

```markdown
### Knowledge

- **AI.VIII.A.K1** — Purpose of and procedures for proper straight-and-level flight
```

The ACS Elements section is a permanent Flight Guide improvement over the Binns format and must not be omitted.

## Lesson Outline

This is the quick oral-teaching roadmap.

It should allow the instructor applicant to glance at the page and immediately understand the teaching sequence.

Keep it concise.

---

# 7. Prepare — Deep Study Without Cluttering the Lesson

The Prepare tab contains the optional deeper study material that would otherwise clutter the simple lesson-plan presentation.

Typical structure:

```markdown
# Prepare

## Primary References

## Video Review

## Visual References Used in This Lesson

## Additional Study
```

Use only the subsections that are useful.

## FAA references

Prefer direct Flight Guide knowledge links and PDF widgets.

Example:

```markdown
- [FAA-H-8083-3 — Airplane Flying Handbook](/knowledge/Airplane_Flying_Handbook.pdf)

[[pdf: /knowledge/Airplane_Flying_Handbook.pdf]]
```

### PDF page ranges

Never guess physical PDF page numbers.

The `start=` and `end=` values used by Flight Guide refer to the actual physical PDF pages used by the application, not a printed page number, chapter page number, index number, or guessed extracted page.

If a range has not been verified:

- embed the full PDF, or
- leave the range unassigned until verified.

A user-confirmed physical range is authoritative.

## Videos

Keep useful videos even when the lesson itself is intentionally concise.

Use exact relevant cuts whenever possible:

```markdown
[[youtube: URL | start=00:25 | end=04:10 | title=Descriptive Title]]
```

Do not guess video timestamps.

If the user supplies chapter timestamps, select the smallest continuous timeframe that covers the Task material.

Videos belong primarily in **Prepare**, not scattered throughout Teach, unless a specific clip is essential at the point of instruction.

## Visual reference inventory

When useful, list the image files used in the lesson so the author can quickly confirm required assets exist.

---

# 8. Teach — The Core Printable Lesson

The Teach tab is the heart of the CFI lesson.

It should preserve the **simple Binns teaching flow** while using Flight Guide visuals and carefully selected enhancements.

## Key rule

**Teach each concept once.**

Do not create separate giant Knowledge, Risk Management, and Skills chapters that repeat the same material.

The Overview maps the ACS K/R/S requirements. Teach integrates those requirements into a natural instructional sequence.

For example, if defense mechanisms involve Knowledge, Risk Management, and Skills, teach defense mechanisms once and incorporate:

- definition,
- aviation example,
- instructor recognition,
- appropriate instructor response.

## Writing style

Teach should be:

- concise,
- technically exact,
- teachable aloud,
- easy to scan,
- aviation-specific,
- useful in a CFI oral,
- efficient when printed in Letter portrait.

Prefer:

- short paragraphs,
- compact bullet lists,
- clear H2/H3 hierarchy,
- aviation examples,
- concise procedures,
- visual aids.

Avoid:

- textbook-length prose,
- repeated explanations,
- unnecessary historical background,
- generic filler,
- excessive web-only decoration.

The printed Overview followed by Teach should read naturally as one continuous lesson document.

Do not write phrases such as:

- “as shown in the Overview tab,”
- “open Prepare,”
- “click the next tab.”

The printed document has no tabs.

---

# 9. Images and Screenshots

Use screenshots and diagrams directly inside **Teach** when they are materially better than making the instructor reopen the source PDF.

Good candidates include:

- FAA diagrams,
- tables,
- models,
- aircraft-control illustrations,
- sight-picture illustrations,
- system diagrams,
- visual teaching aids.

Do not screenshot ordinary prose merely to avoid rewriting it.

Until a dedicated `[[image:]]` authoring widget is confirmed available, use the established raw HTML figure pattern:

```html
<figure class="lesson-reference-figure">
    <img
        src="/knowledge/Filename.png"
        alt="Useful descriptive alt text"
        loading="lazy"
    >
    <figcaption>Concise descriptive caption</figcaption>
</figure>
```

Use the user-provided filename exactly, including unusual extensions or duplicate suffixes.

Place the image immediately after or adjacent to the concept it supports.

Images used in Overview, Teach, or Fly must be suitable for the printable lesson.

---

# 10. Flight Guide Enhancements

Enhancements are encouraged when they improve learning without making the lesson visually busy.

Supported/established examples include:

```text
[[mnemonic: ...]]
[[highlight: ...]]
[[answer: ...]]
[[pdf: ...]]
[[youtube: ...]]
```

## Mnemonics

Use for information that genuinely benefits from recall assistance.

## Highlights

Use sparingly for high-value distinctions, instructor emphasis, risk, or control concepts.

Do not make every paragraph a highlighted card.

## Instructor techniques

If a Flight Guide or user-specific technique is not an FAA-defined term, label it explicitly.

Example:

`### Instructor Technique — Lindbergh Reference`

State that it is a Flight Guide instructional technique rather than an FAA-required term.

---

# 11. Fly — Flight / Maneuver Tasks Only

Use `# Fly` when the ACS Task contains meaningful flight demonstration or maneuver instruction.

The Fly tab is more operational than Teach.

A standard maneuver Fly section should generally contain:

```markdown
# Fly

## Setup

## Instructor Demonstration

## Learner Practice

## Instructor Demonstration Technique

## Analyze and Correct Common Errors

## Completion Standards

## Kneeboard
```

Adjust subsection names when the Task requires it, but preserve the basic sequence:

**setup → demonstrate → learner practice → teach/correct → standards → kneeboard**

## Fly content requirements

Where applicable, include:

- clearing and setup,
- maneuver objective,
- visual references,
- configuration,
- control use,
- power and trim,
- coordination,
- instructor demonstration cues,
- learner practice,
- risk management,
- common-error recognition,
- correction technique,
- completion/performance standards.

The CFI applicant must be able to explain while demonstrating without degrading aircraft control, situational awareness, or collision avoidance.

---

# 12. Common Errors

Common errors are critical in CFI ACS lessons.

Use the best applicable combination of:

- current ACS,
- FAA handbooks,
- Binns lesson,
- user-provided common-error lists,
- appropriate aircraft-specific experience.

Clean obvious transcription errors or wording issues without changing the technical meaning.

## Teach common-error section

For each significant error, use a concise explanation and correction.

Example:

```markdown
### Instrument Chasing

**Error:** Learner continuously reacts to small instrument movements.

**Correction:** Re-establish the outside attitude, allow the airplane to stabilize, then use a brief instrument check to verify performance.
```

## Fly common-error analysis

For flight Tasks, the applicant should be ready for the evaluator to simulate an error.

A useful format is:

```markdown
### Head Inside / Instrument Chasing

**Recognize:** ...

**Correct:** ...
```

Do not merely list the errors; teach how to recognize and correct them.

---

# 13. Kneeboard — Flight Tasks

For applicable flight Tasks, `## Kneeboard` is the **final H2 section inside `# Fly`**.

Use the established Flight Guide compact vertical-rail architecture.

Do not replace it with plain Markdown headings.

Example structure:

```html
<div class="kneeboard-header">
    <strong>TASK NAME — CFI AREA.TASK</strong>
</div>

<div class="kneeboard-layout">

  <div class="kneeboard-group">
    <div class="kneeboard-rail">SETUP</div>
    <div class="kneeboard-group-body">
      <div class="kneeboard-item">
        <label><input type="checkbox"> Action</label>
        <div class="kneeboard-detail"><strong>P:</strong> Concise procedure.</div>
        <div class="kneeboard-detail"><strong>CE:</strong> One high-value common error.</div>
      </div>
    </div>
  </div>

</div>
```

## Kneeboard rules

- Keep checkboxes usable.
- `P:` = concise procedure or teaching cue.
- `CE:` = one high-value common error.
- Do not attempt to put every common error on the kneeboard.
- Keep the full common-error analysis in Teach/Fly.
- Use rails that match the actual task rather than forcing generic labels.
- Keep the kneeboard compact enough to function as a quick cockpit/instructional reference.

Examples of useful rails:

- SETUP
- ATTITUDE
- POWER
- TRIM
- X-CHECK
- TEACH
- ENTRY
- MANEUVER
- RECOVERY
- SAFETY
- ERRORS

---

# 14. Review — Oral / Checkride Review

The Review tab contains concise oral-review questions.

Typical structure:

```markdown
# Review

## Oral / Checkride Review

### 1. Question?

[[answer:
Answer.
]]
```

Use approximately **5–10 high-value questions** depending on Task complexity.

Questions should test:

- key definitions,
- relationships,
- practical application,
- risk management,
- instructional decisions,
- common-error correction,
- ACS-specific expectations.

Every review question must have an `[[answer:]]` block.

Do not scatter dozens of Study Checks throughout Teach unless there is a specific instructional reason. Keep the main teaching flow clean.

---

# 15. Printable-Lesson Authoring Rules

The CFI `Print Lesson` output is intended to resemble a simple, useful Binns-style PDF.

The printable document contains:

1. **Overview**
2. **Teach**
3. **Fly**, if present
4. **Kneeboard**, if present, appended at the end

The printable document excludes:

- Prepare
- Review
- videos
- embedded PDF viewers
- navigation
- tabs/buttons
- other web-only controls

## Authoring implications

Overview, Teach, and Fly must be written so they work as a continuous paper document.

Optimize for Letter portrait printing:

- concise paragraphs,
- compact lists,
- meaningful headings,
- limited unnecessary whitespace,
- images sized for page width,
- avoid very large decorative elements.

The Kneeboard is forced to begin on a new printed page by the application. Author it as a self-contained final reference section.

Do not create a second printable Markdown file.

The same `lesson.md` drives both web and print.

---

# 16. Aircraft-Specific Content

Keep the core lesson valid for ASEL generally.

Use **Cessna 172S / G1000** examples when they improve practical instruction, especially for:

- controls,
- systems,
- trim,
- avionics,
- checklist usage,
- aircraft-specific procedures,
- performance examples.

Do not turn a general ACS principle into a C172-only rule unless the Task is specifically being taught as an aircraft-specific procedure.

When aircraft-specific information matters, verify it against the approved C172S POH.

---

# 17. Risk Management

Risk Management must be taught, not merely copied from the ACS.

For every ACS Risk element:

1. Explain the hazard.
2. Explain how the pilot/instructor recognizes it.
3. Explain the consequence.
4. Explain practical mitigation.
5. Integrate the mitigation into the teaching or flight procedure when applicable.

Do not confuse **risk management** with **common learner errors**.

- Risk Management = hazard, consequence, recognition, mitigation.
- Common Errors = mistakes in learner knowledge or performance and how the instructor corrects them.

---

# 18. ACS Accuracy Rules

Never guess:

- ACS codes,
- required Tasks,
- performance tolerances,
- regulatory requirements,
- POH procedures,
- PDF physical page numbers,
- video timestamps.

Verify them.

When a specific tolerance is applicable, use the current controlling pilot ACS/CFI ACS language rather than memory.

Do not add a tolerance merely because it is commonly associated with the maneuver if the Task does not require it.

---

# 19. Content Density

The goal is **not** to make the longest possible lesson.

The goal is:

> Binns-level clarity and simplicity, with better ACS traceability, better FAA grounding, better visuals, useful videos, and stronger practical teaching aids.

If a concept can be taught accurately in three bullets, do not use three paragraphs.

If a graphic explains the concept faster than prose, use the graphic and concise supporting text.

If optional depth is valuable but would clutter the core lesson, put it in Prepare.

---

# 20. House-Style Reference

Before creating a new CFI ACS lesson, inspect the **latest approved CFI ACS lesson(s)** in the repository and match their established house style.

The initial reference implementation is:

**Area VIII, Task A — Straight-and-Level Flight**

Use it as the model for:

- Overview density,
- Prepare organization,
- Teach hierarchy,
- inline figures,
- Fly structure,
- common-error treatment,
- vertical-rail Kneeboard,
- Review questions,
- overall writing tone.

Do not mechanically copy task-specific content from the reference lesson.

---

# 21. Ground-Only vs Flight Task Decision

## Ground-only Task

Use:

**Overview | Prepare | Teach | Review**

Do not create an empty Fly tab or Kneeboard.

## Flight / maneuver Task

Use:

**Overview | Prepare | Teach | Fly | Review**

Place `## Kneeboard` last inside Fly when a cockpit/instructional quick-reference is useful.

---

# 22. Final Quality-Control Checklist

Before considering a CFI ACS lesson complete, verify all of the following.

## ACS

- [ ] Exact Area and Task title
- [ ] Current ACS Objective represented accurately
- [ ] Every Knowledge element present
- [ ] Every Risk Management element present
- [ ] Every Skill element present
- [ ] Exact current ACS identifiers used
- [ ] Applicable performance standards verified

## Binns alignment

- [ ] Matching Binns lesson reviewed
- [ ] Major Binns teaching topics represented
- [ ] Useful common errors represented
- [ ] Lesson remains simple and teachable
- [ ] No substantial Binns prose copied verbatim

## Sources

- [ ] Applicable FAA references included
- [ ] Actual approved filenames verified
- [ ] PDF ranges verified or omitted
- [ ] Aircraft-specific claims verified against POH when applicable
- [ ] User-provided references incorporated

## Overview

- [ ] Objective
- [ ] Purpose
- [ ] Schedule / Equipment
- [ ] Learner / Instructor Actions
- [ ] Completion Standards
- [ ] ACS Elements
- [ ] Concise Lesson Outline

## Prepare

- [ ] Primary references
- [ ] Useful PDF embeds
- [ ] User-approved or useful videos
- [ ] Exact video cuts where known
- [ ] Optional deeper study kept out of Teach

## Teach

- [ ] Natural instructional sequence
- [ ] Concepts taught once rather than repeated under K/R/S
- [ ] Aviation-specific examples
- [ ] Risk management integrated
- [ ] Common errors and corrections included where applicable
- [ ] Useful screenshots/diagrams placed inline
- [ ] Concise enough for portrait printing

## Fly, when applicable

- [ ] Setup
- [ ] Instructor demonstration
- [ ] Learner practice
- [ ] Instructor teaching cues
- [ ] Risk management
- [ ] Common-error recognition and correction
- [ ] Completion standards
- [ ] Kneeboard last

## Kneeboard, when applicable

- [ ] Existing vertical-rail HTML architecture used
- [ ] Concise `P:` procedure lines
- [ ] High-value `CE:` lines
- [ ] Checkboxes retained
- [ ] Suitable as a quick cockpit teaching reference

## Review

- [ ] Approximately 5–10 useful oral/checkride questions
- [ ] Every question has an `[[answer:]]`

## Print readiness

- [ ] Overview → Teach → Fly reads naturally as one document
- [ ] No tab-dependent wording in printable content
- [ ] Images are useful and printable
- [ ] No unnecessary web-only material in printable sections
- [ ] Kneeboard is self-contained for its forced new print page

---

# 23. Standard Prompt for a New CFI ACS Lesson

Use a short authoring prompt because the detailed rules live in this protocol:

```text
Work on CFI ACS Area [AREA], Task [TASK] — [TITLE].

Follow the CFI ACS Lesson Authoring Protocol. Review the current ACS Task, the matching Binns lesson, the approved FAA sources, and the latest approved CFI ACS lesson for house style. Incorporate the user-provided images/videos/references exactly where relevant and build the complete lesson.md.
```

If the user requests **alignment before generation**, do not generate the final `lesson.md` until the user approves the alignment.

---

# 24. Permanent Distinction From Other Flight Guide Content

Do not blur these three products:

### CFI ACS

**ACS-organized lesson plans** designed for CFI oral/practical preparation and teaching demonstration.

### Private / Instrument / Commercial ACS

**ACS-organized study guides** unless the user explicitly establishes another format.

### Training Syllabi

**Sequential real-student training lesson plans** organized by training progression rather than ACS Task order.

The same aviation subject may appear in more than one product for a different purpose. That is intentional.
