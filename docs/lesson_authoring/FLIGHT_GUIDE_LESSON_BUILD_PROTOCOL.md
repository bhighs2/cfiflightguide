# Flight Guide Lesson Build Protocol

## Purpose

## Agent Operating Contract

This protocol is designed so the user can invoke lesson development with a **short prompt**, such as:

> Work on Private Lesson 2 — Airport Environment, Communications and Surface Operations.

When given a lesson-development request, the authoring agent should handle the detailed workflow from this protocol automatically.

### On every new lesson request

The agent should:

1. Read this protocol.
2. Read the Source Alignment Worksheet.
3. Read the canonical lesson template.
4. Inspect the actual syllabus structure and the most relevant adjacent/completed lessons in the repo.
5. Treat the most recently approved completed lesson as the **house-style reference** for:
   - lesson density,
   - Fly-section organization,
   - visible H3/H4 hierarchy,
   - full procedures and common errors,
   - kneeboard HTML structure,
   - checkbox behavior,
   - `P:` / `CE:` shorthand,
   - debrief structure,
   - and overall level of detail.
6. Determine the lesson's likely scope, prior-learning dependencies, and later-lesson boundaries.
7. Inspect the available approved knowledge sources in the repo.
8. Proactively suggest relevant:
   - PDFs and exact page ranges,
   - images and diagrams,
   - videos,
   - mnemonics and memory aids,
   - attention/highlight items,
   - risk-management topics,
   - procedures,
   - primary-source common errors,
   - scenarios,
   - kneeboard content.
9. Work through source alignment collaboratively with the user.
10. **Do not generate the final `lesson.md` until the user explicitly approves generation.**
11. After approval, generate the lesson using the canonical template and run the Final Lesson QA checklist.

### Interaction style

The agent should **not** make the user restate this protocol in every prompt.

The agent should drive the alignment process intelligently from the lesson title, syllabus position, adjacent lessons, and available source files.

Ask only for information that cannot reasonably be determined from the repo or proposed for user approval.

Do not silently invent missing source material or aircraft-specific values.

Do not jump directly to a polished lesson simply because the lesson title is known.

---


This file is the permanent build standard for creating Flight Guide training lessons.

Use it **before drafting any new `lesson.md`**.

The objective is to prevent premature lesson generation, source gaps, duplicated content, inconsistent structure, and unclear ownership between adjacent lessons.

---

# 1. Non-Negotiable Workflow

## Phase 1 — Define the Lesson

Before writing lesson content, establish:

- Lesson number.
- Lesson title.
- Stage.
- Lesson type:
  - GROUND
  - GROUND + FLIGHT
  - SOLO
  - EVALUATION
- Target proficiency:
  - Introduced
  - Developing
  - Proficient
  - ACS Ready
  - Needs Additional Training
- Primary lesson objective.
- Completion standard.
- What this lesson **owns**.
- What this lesson only **introduces**.
- What is explicitly deferred to later lessons.
- What prior lesson knowledge or skill this lesson builds on.

Do not draft the full lesson until these boundaries are clear.

---

# 2. Adjacent-Lesson Boundary Check

For every major topic, identify:

| Topic | Introduced Here? | Taught Here? | Practiced Here? | Mastered Later? | Later Lesson |
|---|---:|---:|---:|---:|---|
| Example | Yes | Basic | Yes | Yes | Lesson XX |

Use this to prevent one lesson from becoming overloaded.

A topic may appear in multiple lessons if its **level of learning changes**.

Example:

- Lesson 1 — identify the pitot/static openings.
- Lesson 13 — understand the pitot-static system.
- Lesson 19 — use and interpret the instruments.
- Lesson 20 — manage failures.

That is intentional progression, not duplication.

---

# 3. Course Continuity / Connection Rule

Every lesson must visibly connect to the course around it.

This is not optional background reasoning. The finished lesson should help the learner and instructor understand:

1. **Where we came from.**
2. **What advances in this lesson.**
3. **Where this is going next.**

## Builds On

Every lesson after Lesson 0 should identify the specific prior lesson or lessons that provide prerequisite knowledge, habits, or skills.

Use actual lesson numbers and titles.

Example:

```markdown
## Course Connection

### Builds On

**Lesson 1 — Aircraft Familiarization, Preflight and Basic Control**

This lesson builds on:

- basic taxi steering and braking,
- conservative taxi speed,
- checklist discipline,
- outside visual orientation,
- positive control transfer.
```

Do not write vague language such as "previous lessons."

## Leads To

Every lesson except the final course lesson should identify the later lesson or lessons that depend on the current material.

Example:

```markdown
### Leads To

**Lesson 3 — Traffic Pattern, Takeoffs, Landings and Go-Arounds**

The airport-surface awareness, communications, and runway-incursion-avoidance skills developed here are prerequisites for safe traffic-pattern operations.
```

## Progression of Repeated Skills

When a topic appears in multiple lessons, make the progression explicit.

Example:

```text
Lesson 1 → INTRODUCED
Basic taxi control

Lesson 2 → DEVELOPING
Taxi routes, signs, markings, clearances, wind correction

Lesson 3 → APPLIED
Taxi to and from an active traffic-pattern operation
```

Repeated content should advance the learner's level of understanding or performance rather than simply repeat the same treatment.

## Review of Prior Learning

The Brief should contain a specific **Review of Prior Learning** subsection that names the prior lesson and identifies only the knowledge or skills needed for the current lesson.

Example:

```markdown
### Review of Prior Learning

From **Lesson 1 — Aircraft Familiarization, Preflight and Basic Control**, review:

- Basic taxi steering and braking.
- Conservative taxi speed.
- Checklist discipline.
- Positive exchange of flight controls.
- Outside visual scanning.
```

## Continuity Rule for the Agent

During source alignment, the authoring agent must inspect the adjacent lessons and propose the course connection before final lesson generation.

The user should not have to manually remind the agent to connect lessons.

---

# 4. Regulatory / ACS Alignment Gate

Before drafting, identify all applicable:

- 14 CFR Part 61 requirements.
- 14 CFR Part 91 requirements where relevant.
- Private Pilot ACS Areas of Operation and Tasks.
- Any required endorsements.
- Aircraft-specific operating limitations where appropriate.
- FAA handbook chapters/pages.
- Advisory circulars where useful.

Do not write vague mappings such as "covered in Brief."

Map each required element to a specific lesson section or skill.

---

# 5. Source Alignment — Do This Before Writing

The assistant/author should stop and align on source material with the user before generating the final lesson.

For each category below:

1. Identify what is already available.
2. Suggest useful additions.
3. Ask the user to approve, add, remove, or replace materials.
4. Only after alignment, proceed to lesson generation.

---

## 4A. PDF / Document Sources

For every relevant source, record:

- Exact local filename.
- Friendly display name.
- Chapter or section.
- Exact page range.
- Why the learner needs it.
- Whether it belongs in:
  - Prepare
  - Brief
  - Fly
  - Reference only

Preferred source hierarchy:

1. Applicable FAA regulations.
2. Applicable ACS.
3. FAA handbooks.
4. Aircraft POH / AFM.
5. FAA advisory circulars.
6. Manufacturer guidance.
7. Other high-quality instructional material when needed.

### What to Look For in PDFs

Look specifically for:

- Definitions.
- Procedures.
- Diagrams.
- Limitations.
- Common errors.
- Risk-management guidance.
- Completion standards.
- Tables.
- Aircraft-specific systems.
- Examples or scenarios.
- Figures that materially improve understanding.

### Source Presence Rule

Before claiming that an approved source is missing, inspect the actual filenames in `knowledge/approved/`.

Do **not** treat absence from a text index, search index, extracted-text cache, or workspace semantic search as proof that the PDF is not present.

If the file exists but its binary content or page map cannot be inspected, say:

> File present; page mapping not yet verified.

Do not say the source is unavailable.

### PDF Page-Number Integrity Rule

Flight Guide PDF embeds must use the **actual physical PDF page positions required by the application**, not a guessed book page number, chapter page number, extracted-text page label, search-index page number, or table-of-contents number.

Before proposing an exact `start=` or `end=` value:

1. Inspect the actual source PDF file.
2. Determine the physical PDF page index/position that Flight Guide will serve.
3. Compare it with any printed page number shown on the document.
4. Record both when they differ.
5. Use only the physical PDF page position for the embed.

Example:

```text
Printed handbook page: 14-12
Physical PDF page: 356
Flight Guide embed start: 356
```

If the physical PDF page mapping cannot be verified, **do not guess an exact range**.

Instead record:

```text
Chapter / section: Airport Signs and Markings
Physical PDF pages: UNVERIFIED — USER CONFIRMATION REQUIRED
```

and leave the `[[pdf: ... | start=... | end=...]]` syntax out until the range is verified.

A user-confirmed physical PDF page range is authoritative and should not be replaced by an inferred range.

### PDF Embed Rule

After the physical PDF page range has been verified, use:

```markdown
[[pdf: /knowledge/FILENAME.pdf | start=XX | end=YY]]
```

Do not duplicate the same large embed repeatedly without a teaching reason.

Use the source at the point where it is most useful.

A source may contain material that is useful both now and later. When appropriate, identify:

- **Lesson focus now** — the portion directly relevant to the current lesson.
- **Future reference** — useful sections that will become more important in later lessons.

Example: a sample-radio-calls reference may support taxi/Class D calls now while also serving as future review for arrivals, Class B, or flight following.

The site lazy-loads PDF source cards, so media-heavy lessons remain viable, but unnecessary duplicate references should still be avoided.

---

## 4B. Images / Diagrams

Images should solve a specific instructional problem.

Good reasons to include an image:

- Show where something is physically located.
- Show a cockpit control or instrument.
- Show aircraft markings or documents.
- Show airflow or aerodynamic relationships.
- Show an airport marking/sign.
- Show a system diagram.
- Compare correct vs incorrect visual pictures.
- Show a sight picture or visual reference.
- Show an aircraft-specific configuration.

Avoid decorative imagery that does not improve learning.

### Image Checklist

For each proposed image:

- What concept does it clarify?
- Is it aircraft-specific?
- Does the learner need to recognize it visually?
- Is the image already in `knowledge/approved`?
- What is the exact filename?
- What alt text should be used?
- What caption should explain why it matters?

Recommended markup:

```html
<figure class="lesson-reference-figure">
    <img
        src="/knowledge/example_image.jpeg"
        alt="Clear description of the instructional image"
    >
    <figcaption>
        Short instructional caption explaining what the learner should notice.
    </figcaption>
</figure>
```

---

## 4C. Videos

Videos are instructional aids, not filler.

### Video Discovery Rule

Video alignment is a required consideration for every lesson. The agent should not skip video suggestions merely because no approved video is already stored in the repository.

For each lesson:

1. Identify the concepts that would materially benefit from seeing or hearing a real demonstration.
2. Proactively suggest useful video targets.
3. If web/video search is available, propose actual candidate videos with:
   - title,
   - channel/publisher,
   - URL,
   - why it is useful,
   - what the learner should watch for,
   - useful start/end segment when known.
4. Prefer FAA material or reputable flight-training/instructor sources when they fit.
5. If web/video search is not available, give the user **specific search targets**, for example:
   - "towered airport taxi clearance cockpit example"
   - "runway incursion hold-short markings training"
   - "quartering tailwind taxi control C172"
6. Mark the category **PENDING VIDEO SELECTION** until the user approves a candidate or explicitly chooses no video.

Do not default to "proceed with text/PDF only" simply because a video is not already in the repo.

For every video, identify:
- URL.
- Title.
- Publisher / channel.
- Why it belongs in this lesson.
- What the learner should specifically watch for.
- Useful start/end times if only an excerpt is relevant.

Use:

```markdown
[[youtube: URL | start=... | end=... | title=...]]
```

or:

```markdown
[[youtube: URL | title=...]]
```

### What to Look For in Videos

Prefer videos that demonstrate:

- Real cockpit sight pictures.
- Instructor demonstrations.
- Control inputs and aircraft response.
- Procedures difficult to understand from text alone.
- Common mistakes.
- Scenario-based decision making.
- Aircraft-specific operations.
- Visual references.

A lesson usually needs only the videos that materially improve understanding.

Do not add multiple videos that teach the exact same thing unless they provide meaningfully different perspectives.

---

# 6. Memory and Attention Tools

## Mnemonics / Memory Aids

Use a mnemonic when the learner genuinely benefits from recalling a sequence, framework, or relationship.

Syntax:

```markdown
[[mnemonic:
NAME |
Meaning or expansion.
]]
```

Examples:

- ARROW
- IMSAFE
- CONTROL → HOLD → TRIM
- ATTITUDE + POWER = PERFORMANCE

### Mnemonic Rule

Yellow mnemonic = **remember this**.

Do not create a mnemonic simply because a list exists.

---

## Highlight / Attention Items

Use a blue highlight when the learner needs to pause and pay particular attention to an idea.

Syntax:

```markdown
[[highlight:
Key Point |
Important instructional content.
]]
```

Useful labels include:

- Attention
- Key Point
- Safety
- Instructor Emphasis
- Motivation
- Visual Flying
- Key Distinction
- Risk Management
- Technique

### Highlight Rule

Blue highlight = **pay particular attention to this concept**.

It is different from a mnemonic.

Do not overuse highlights. If everything is highlighted, nothing is highlighted.

---

# 7. FAA Lesson-Plan Structure

Every Flight Guide lesson must clearly contain:

- Objective.
- Content that supports the objective.
- Completion standards.

The instructional flow should also reflect:

1. Preparation.
2. Presentation.
3. Application.
4. Review and Evaluation.

Flight Guide maps this into:

- Overview
- Prepare
- Brief
- Fly
- Debrief

Not every lesson requires every tab.

---

# 8. Standard Lesson Architecture

## OVERVIEW

Use for:

- Lesson objective.
- Completion standards.
- Why this matters.
- **Course Connection: Builds On / Leads To.**
- Regulatory / ACS alignment.
- References.
- Relationship to the course.
- Instructional approach when useful.

---

## PREPARE

Use for learner preparation before instruction:

- Assigned reading.
- PDFs.
- Videos.
- Images.
- Memory aids.
- Key concepts.
- Study questions.
- Aircraft-specific preparation.

Prepare should tell the learner **what to study and what to look for**.

Do not merely dump source links.

---

## BRIEF

Permanent H2 structure:

```markdown
# Ground Brief

## Brief Setup
## Knowledge
## Risk Management
## Skills
## Scenario Application
## Review and Evaluation
```

### Brief Setup

Usually includes:

- Objective.
- Completion Standard.
- Estimated Time.
- Instructional Method.
- Review of Prior Learning.
- Equipment.
- Introduction.
- Attention.
- Motivation.

### Knowledge

Teach concepts and understanding.

### Risk Management

Risk Management is:

- Hazard.
- Consequence.
- Recognition.
- Mitigation.

Risk Management is **not** the common-errors section.

### Skills

Each applicable skill should normally use:

```markdown
### Skill Name

#### Purpose

#### Procedure

#### Instructor Demonstration

#### Learner Practice

#### Common Errors

#### Completion Standard
```

If the FAA Airplane Flying Handbook or other primary source contains an explicit common-errors list, use that FAA list as the backbone.

Do not replace an FAA common-error list with a made-up abbreviated list in the full Brief or Fly section.

### Scenario Application

Use realistic situations to require the learner to:

- recognize hazards,
- gather information,
- make decisions,
- communicate uncertainty,
- apply knowledge,
- explain why.

State the expected proficiency level.

### Review and Evaluation

Include:

- Review Questions.
- Answers.
- Instructor Evaluation.
- Next Assignment.

**Review Questions must always include answers.**

Use:

```markdown
[[answer:
1. ...
2. ...
]]
```

---

# 9. Flight-Lesson Air Work Continuity Rule

For every **GROUND + FLIGHT** lesson, the Fly section must contain an intentional airborne training plan unless the lesson is explicitly approved as a surface-only/ground-only exception.

Do not omit airborne work merely because the lesson's primary new objective is on the ground or airport surface.

## If the Lesson Introduces New Air Work

Include the new maneuver/skill with:

- purpose,
- procedure,
- instructor demonstration,
- learner practice,
- all relevant primary-source common errors,
- and completion standard.

## If the Lesson Introduces No New Air Work

Create an explicit section titled:

```markdown
## Air Work Reinforcement
```

Reinforce the most relevant prior flight skills.

For an early Private Pilot lesson, this will often mean repeating previously introduced fundamentals such as:

- outside-reference attitude flying,
- straight-and-level flight,
- level turns,
- climbs,
- descents,
- trim,
- and coordination.

The reinforcement must show progression. It should not simply copy the prior lesson unchanged.

Examples of progression:

- less instructor prompting,
- more learner verbalization,
- improved outside-reference use,
- better coordination,
- earlier trim use,
- improved scan,
- increased workload tolerance,
- or application while handling new communication/situational-awareness demands.

The lesson should state explicitly:

- **Primary lesson target**
- **Secondary airborne reinforcement target**

This keeps the course flying continuously while new ground/surface concepts are introduced.

---

# 10. FLY Section Standard

The Fly section is the **full instructional flight card**, not the kneeboard.

It should be operational and usable by an instructor in the airplane.

For a GROUND + FLIGHT lesson, the Fly section should normally follow the actual flight sequence:

1. Preflight / cockpit.
2. Engine start / taxi.
3. Surface or departure work.
4. Before takeoff.
5. **Air Work** or **Air Work Reinforcement**.
6. Return / runway exit / taxi.
7. Shutdown / secure.
8. Flight completion criteria.
9. Kneeboard.

Do not build a flight card that stops at the runway unless the lesson is intentionally approved as a surface-only event.

Typical H2 organization:

```markdown
# Flight Card

## Flight Setup
## Preflight and Cockpit
## Engine Start and Basic Taxi
## Before Takeoff and Departure
## Basic Air Work
## Return, Shutdown and Securing
## Flight Completion Criteria
## Kneeboard
```

Use only the sections appropriate to the lesson.

---

## Fly Skill Standard

For each flight maneuver or procedural item, include enough information to conduct instruction.

Use:

```markdown
### Maneuver / Skill

#### Procedure

1. ...
2. ...
3. ...

#### Common Errors

1. ...
2. ...
3. ...

#### Instructor Demonstration / Learner Practice

- ...
```

### Important

In the full Fly section:

- Include **all relevant primary-source common errors** when an FAA source provides them.
- Include the relevant procedure.
- Include instructor emphasis where helpful.
- Do not reduce the Fly section to kneeboard shorthand.

---

# 11. Kneeboard Standard

The kneeboard is a **separate abbreviated operational extract**.

It is not a copy of the Fly section.

The approved Flight Guide kneeboard uses the existing **HTML vertical-rail architecture**. Do not replace it with ordinary Markdown headings and bullets.

Use the most recently approved lesson kneeboard as the structural reference.

Required architecture:

```html
<div class="kneeboard-header">...</div>

<div class="kneeboard-layout">

    <div class="kneeboard-group">
        <div class="kneeboard-rail">SECTION</div>
        <div class="kneeboard-group-body">

            <div class="kneeboard-item">
                <label><input type="checkbox"> <strong>ITEM</strong></label>
                <div class="kneeboard-detail"><strong>P:</strong> ...</div>
                <div class="kneeboard-detail"><strong>CE:</strong> ...</div>
            </div>

        </div>
    </div>

</div>
```

Rails may change to fit the lesson, but the structure should remain consistent.

For a GROUND + FLIGHT lesson with airborne work, include an `AIR WORK` rail unless the user explicitly approves otherwise.

The physical print target is:

- Letter landscape.
- 11 × 8.5 inch printed sheet.
- Kneeboard content occupies the left 5.5 × 8.5 inch half.
- Right half remains blank.
- Content may flow onto additional landscape sheets.

---

## Kneeboard Content Rules

Use:

- Open checkboxes.
- Very short phrases.
- Checklist references instead of duplicating aircraft checklist items.
- Abbreviated procedure.
- One high-value common error.
- Memory cues only when useful.

Preferred abbreviations:

- `P:` = Procedure
- `CE:` = Common Error

For communication-heavy lessons, the kneeboard may also include a compact `RADIO` rail with short operational examples or call patterns.

When doing so:

- keep calls concise,
- use user-approved/localized airport, aircraft call sign, ramp, runway, taxi route, and direction-of-flight details,
- do not invent local taxi routes or airport-specific phraseology,
- distinguish pilot call, ATC response, and readback when useful,
- and treat examples as patterns rather than scripts to memorize.

Example:

```text
☐ CLIMBS
  P: Power + attitude → coordinate → confirm → trim → lead level-off
  CE: Chasing airspeed instead of holding climb attitude
```

### Do Not Duplicate the Aircraft Checklist

If the C172S checklist already covers:

- fuel quantity,
- oil,
- flight controls,
- tires,
- brakes,
- propeller,
- openings,
- seat belts,
- configuration,

the Flight Guide kneeboard should normally say:

```text
☐ C172S checklist
```

and only add lesson-specific instructor cues that the aircraft checklist does not provide.

---

## Kneeboard Section Rail

Use compact vertical section rails.

Current preferred labels:

- PREFLT
- START/TAXI
- BEFORE T/O
- AIR WORK
- RETURN

Horizontal separators should run across the full kneeboard width.

---

# 12. Common Errors Rule

There are two levels:

## Full Brief / Fly

Use all relevant FAA/common-source errors.

Example:

```markdown
#### Common Errors

FAA-highlighted common errors include:

1. ...
2. ...
3. ...
```

## Kneeboard

Use only **one high-value common error** per maneuver.

Example:

```text
CE: Chasing instruments instead of the natural horizon.
```

Choose the error most likely to help the learner or instructor during that specific flight.

---

# 13. Procedures Rule

Procedures should be:

- Safe.
- Chronological.
- Appropriate to the target proficiency.
- Aircraft-specific only when verified.
- Written to support actual instruction.

Do not invent:

- airspeeds,
- power settings,
- capacities,
- limitations,
- configuration values,

from memory.

Use the POH/checklist when exact aircraft-specific values matter.

---

# 14. Aircraft-Specific Content Rule

For Cessna 172S content:

- Use the C172S POH and checklist.
- Avoid duplicating checklist content on the kneeboard.
- Add Flight Guide cues only when they improve instruction.
- Clearly distinguish:
  - universal flying principles,
  - FAA guidance,
  - C172S-specific procedures,
  - instructor techniques.

---

# 15. Instructor Technique Rule

If using a non-FAA teaching technique, identify it honestly.

Example:

The Lindbergh Reference is an instructor technique used to reinforce FAA concepts of attitude flying and outside visual references.

Do not present instructor-created or third-party terminology as an FAA-required term.

---

# 16. Lesson Scope Rule

Every lesson should have reasonable scope.

Use these categories:

- Introduce.
- Develop.
- Refine.
- Evaluate.

If a topic belongs primarily to a later lesson, say so explicitly.

A first lesson may expose the learner to many items without requiring mastery.

---

# 17. Scenario Progression

Scenarios should become more subtle as training progresses.

Early lessons:

- obvious hazard,
- instructor prompting acceptable,
- learner participates in decision.

Later lessons:

- multiple competing hazards,
- less prompting,
- learner independently identifies and mitigates risk.

---

# 18. Source Suggestions the Assistant Should Offer

Before lesson generation, actively suggest potential useful materials such as:

- Exact FAA handbook chapter/page ranges.
- ACS task references.
- POH sections.
- Useful diagrams.
- Aircraft photographs.
- Cockpit/control images.
- Airport diagrams.
- Weather graphics.
- High-quality demonstration videos.
- Mnemonics.
- Memory aids.
- Attention boxes.
- Safety notes.
- Scenario ideas.
- Common-error sections.
- Learner review questions.

Suggestions are proposals, not automatic inclusions.

The user should have the opportunity to accept, reject, or provide better material.

---

# 19. Source Alignment Gate

Do **not** generate the final `lesson.md` until this gate is complete.

Confirm:

- [ ] Lesson scope approved.
- [ ] Adjacent lesson boundaries approved.
- [ ] Course Connection approved: Builds On / Leads To.
- [ ] Repeated-skill progression identified where applicable.
- [ ] FAA/ACS/regulatory mappings aligned.
- [ ] PDF sources aligned.
- [ ] Every PDF embed page range is verified against the actual physical PDF page positions, or clearly marked UNVERIFIED with no guessed `start/end`.
- [ ] Actual `knowledge/approved/` filenames were checked before any source was called missing.
- [ ] Images aligned.
- [ ] Video needs were actively considered and candidates/search targets were proposed.
- [ ] Videos aligned, intentionally omitted by user, or explicitly marked PENDING VIDEO SELECTION.
- [ ] Mnemonics aligned.
- [ ] Highlights / attention items aligned.
- [ ] Risk-management topics aligned.
- [ ] Skill procedures aligned.
- [ ] Common errors aligned.
- [ ] Scenario ideas aligned.
- [ ] Aircraft-specific references aligned.
- [ ] Review-question scope aligned.
- [ ] Kneeboard content concept aligned.

Only then generate the final lesson.

---

# 20. Final Lesson QA

Before delivering a lesson, verify:

## Content

- [ ] Objective is clear.
- [ ] Completion standard is measurable.
- [ ] Lesson has reasonable scope.
- [ ] Source material supports the content.
- [ ] No invented aircraft-specific values.
- [ ] Regulatory mappings are explicit.
- [ ] Risk Management is distinct from Common Errors.
- [ ] Review Questions have answers.
- [ ] Adjacent lesson boundaries are respected.
- [ ] Course Connection names specific prior and next lessons.
- [ ] Review of Prior Learning names the relevant prior lesson(s).
- [ ] Repeated skills clearly advance rather than merely repeat.

## Prepare

- [ ] Reading tells learner what to look for.
- [ ] Video descriptions tell learner what to watch for.
- [ ] PDFs use only verified physical PDF page positions for `start/end`.
- [ ] No page range was inferred solely from indexed/extracted/printed page numbers.
- [ ] Images have a teaching purpose.
- [ ] Video selections or search targets were actively considered.
- [ ] Mnemonics are useful, not decorative.

## Brief

- [ ] Knowledge is sufficiently developed.
- [ ] Risk Management includes hazard and mitigation.
- [ ] Skills contain procedures.
- [ ] FAA common errors are included where available.
- [ ] Scenarios require application.

## Fly

- [ ] Flight sequence is operationally usable from preflight through return/shutdown.
- [ ] Every GROUND + FLIGHT lesson has Air Work or Air Work Reinforcement unless explicitly approved otherwise.
- [ ] If no new airborne maneuver is introduced, prior skills are intentionally reinforced with progression rather than omitted.
- [ ] Primary lesson target and secondary airborne reinforcement target are clear.
- [ ] Procedures are present.
- [ ] All relevant common errors are present.
- [ ] Instructor emphasis is clear.
- [ ] Target proficiency is appropriate.

## Kneeboard

- [ ] Uses the approved HTML `.kneeboard-header` / `.kneeboard-layout` / `.kneeboard-group` vertical-rail structure.
- [ ] Does not regress to plain Markdown `### PREFLT` style headings.
- [ ] Open checkboxes.
- [ ] Compact section rails match the actual flight sequence.
- [ ] `AIR WORK` rail is present for applicable GROUND + FLIGHT lessons.
- [ ] Communication-heavy lessons use a compact `RADIO` rail when operationally useful.
- [ ] Local radio examples use only user-approved airport/callsign/runway/taxi-route details.
- [ ] No unnecessary checklist duplication.
- [ ] `P:` used for abbreviated procedure.
- [ ] `CE:` used for one high-value common error.
- [ ] Fits the intended 5.5 × 8.5 inch left-half format.

## Architecture

- [ ] Existing custom Markdown syntax preserved.
- [ ] PDF sources lazy-load.
- [ ] YouTube media lazy-loads.
- [ ] No unnecessary duplicate media embeds.

---

# 21. Permanent Principle

The lesson should be detailed enough that another competent instructor could use it to conduct the same instructional period, while remaining flexible enough to adapt to the learner, aircraft, weather, and actual training conditions.

Flight Guide is not merely a study guide.

It is:

- a syllabus,
- an instructor lesson plan,
- a learner preparation tool,
- a flight instructional card,
- a kneeboard aid,
- and a debrief framework.

Every lesson should support those roles without unnecessarily duplicating information.
