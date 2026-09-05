# Flight Guide Lesson Authoring Reference

Use these files together.

## 1. `FLIGHT_GUIDE_LESSON_BUILD_PROTOCOL.md`

Permanent rules for how Flight Guide lessons are researched, aligned, structured, generated, and quality-checked.

This should be treated as the main authoring standard.

## 2. `FLIGHT_GUIDE_SOURCE_ALIGNMENT_WORKSHEET.md`

Copy this for every new lesson.

Complete the worksheet collaboratively **before** generating the full lesson.

The key rule is the **Source Alignment Gate**: do not jump directly from a lesson title to a finished lesson.

First align on:

- scope,
- adjacent lesson ownership,
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
- kneeboard items.

## 3. `FLIGHT_GUIDE_LESSON_TEMPLATE.md`

Canonical copy-ready `lesson.md` structure.

Use it only after the alignment worksheet is approved.

---

# Recommended Workflow for Every New Lesson

1. State the lesson number/title.
2. Open the Source Alignment Worksheet.
3. Establish scope and boundaries.
4. Build the Course Continuity map: **Builds On → Current Lesson → Leads To**.
5. Align FAA/ACS/regulatory requirements.
6. Review PDF sources and exact page ranges.
7. Suggest and approve useful images.
8. Suggest and approve useful videos.
9. Identify mnemonics and memory aids.
10. Identify attention/safety/highlight items.
11. Identify Risk Management topics.
12. Identify skills and procedures.
13. Pull all available FAA/source Common Errors.
14. Develop scenario applications.
15. Plan the abbreviated kneeboard.
16. Mark the worksheet **READY TO GENERATE**.
17. Generate the complete `lesson.md`.
18. Run the Build Protocol QA checklist.

This preserves the workflow:

**ALIGN FIRST → BUILD SECOND → QA THIRD**

---

# Minimal Agent Invocation

Once these files are in the repo and referenced by Copilot instructions, a normal lesson-development prompt should be short.

Example:

```text
Work on Private Lesson 2 — Airport Environment, Communications and Surface Operations.

Follow the Flight Guide lesson-authoring docs. Start with source alignment and do not generate the final lesson.md until I approve it.
```

The authoring docs—not the prompt—should carry the detailed process.
---

# Source-Alignment Guardrails

Two rules are permanent:

1. **Never guess PDF embed page numbers.** `start=` / `end=` are added only after the actual physical PDF page positions are verified against the real source file. Search-index, extracted-text, printed-book, or table-of-contents page numbers are not sufficient by themselves.

2. **Always consider video deliberately.** The absence of an approved video in the repo is not a reason to skip the category. Propose actual candidates when search is available; otherwise propose specific search targets and keep video marked `PENDING VIDEO SELECTION` until the user approves a video or explicitly chooses none.

---

# Flight-Card and Kneeboard House Style

For every new **GROUND + FLIGHT** lesson:

- Do not stop the Fly section at surface operations.
- Include either **Air Work** or **Air Work Reinforcement**.
- If there is no new airborne maneuver, deliberately repeat prior lesson airwork with a progression target.
- Use the approved HTML vertical-rail kneeboard architecture from the most recently approved lesson.
- Do not regress to plain Markdown kneeboard headings/bullets.
- Include an `AIR WORK` kneeboard rail when airborne work is part of the lesson.
- Add lesson-specific rails such as `SURFACE` or `RADIO` when they improve operational usefulness.
- Local radio-call examples must use user-confirmed airport, callsign, ramp, runway, taxi route, and related details.

