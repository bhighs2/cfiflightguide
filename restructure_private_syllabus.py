from pathlib import Path
from datetime import datetime
import shutil


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

TRAINING_ROOT = (
    PROJECT_ROOT
    / "content"
    / "training_syllabi"
)

PRIVATE_ROOT = (
    TRAINING_ROOT
    / "private"
)


# =========================================================
# SYLLABUS
# =========================================================

SYLLABUS = {

    "00_Stage 0. Course Orientation": [

        (
            "00_Lesson 0. Course Orientation and Training Expectations",
            "GROUND",
        ),

    ],


    "01_Stage I. Pre-Solo Foundations": [

        (
            "01_Lesson 1. Aircraft Familiarization, Preflight and Basic Control",
            "GROUND + FLIGHT",
        ),

        (
            "02_Lesson 2. Airport Environment, Communications and Surface Operations",
            "GROUND + FLIGHT",
        ),

        (
            "03_Lesson 3. Traffic Pattern, Takeoffs, Landings and Go-Arounds",
            "GROUND + FLIGHT",
        ),

        (
            "04_Lesson 4. Airspace, Local Operations and Pre-Solo Regulations",
            "GROUND",
        ),

        (
            "05_Lesson 5. Aerodynamics, Slow Flight and Stalls",
            "GROUND + FLIGHT",
        ),

        (
            "06_Lesson 6. Wind Correction and Ground Reference Maneuvers",
            "GROUND + FLIGHT",
        ),

        (
            "07_Lesson 7. Emergencies, Engine-Failure Approaches and Slips",
            "GROUND + FLIGHT",
        ),

        (
            "08_Lesson 8. Crosswind Operations and Landing Refinement",
            "GROUND + FLIGHT",
        ),

        (
            "09_Lesson 9. Pre-Solo Knowledge Test and Review",
            "GROUND · EVALUATION",
        ),

        (
            "10_Lesson 10. Pre-Solo Flight Proficiency Check",
            "GROUND + FLIGHT · EVALUATION",
        ),

        (
            "11_Lesson 11. First Solo",
            "SOLO",
        ),

    ],


    "02_Stage II. Post-Solo Proficiency and Core Ground Knowledge": [

        (
            "01_Lesson 12. Local Solo Consolidation",
            "SOLO",
        ),

        (
            "02_Lesson 13. Aircraft Systems, Instruments and Powerplant",
            "GROUND",
        ),

        (
            "03_Lesson 14. Aircraft Performance, Weight and Balance, and Density Altitude",
            "GROUND",
        ),

        (
            "04_Lesson 15. Steep Turns and Precision Aircraft Control",
            "GROUND + FLIGHT",
        ),

        (
            "05_Lesson 16. Short-Field and Soft-Field Operations",
            "GROUND + FLIGHT",
        ),

        (
            "06_Lesson 17. Aeromedical Factors, ADM and Risk Management",
            "GROUND",
        ),

        (
            "07_Lesson 18. Regulations, Privileges, Limitations, NTSB and AIM",
            "GROUND",
        ),

        (
            "08_Lesson 19. Basic Instrument Flight I",
            "GROUND + FLIGHT",
        ),

        (
            "09_Lesson 20. Emergency Operations and Systems Malfunctions",
            "GROUND + FLIGHT",
        ),

        (
            "10_Lesson 21. Local Solo Proficiency and Experience Builder",
            "SOLO",
        ),

    ],


    "03_Stage III. Weather, Navigation and Cross-Country": [

        (
            "01_Lesson 22. Weather Theory and Aviation Weather Hazards",
            "GROUND",
        ),

        (
            "02_Lesson 23. Weather Services, Reports, Forecasts and Flight Briefing",
            "GROUND",
        ),

        (
            "03_Lesson 24. VFR Charts, Airspace Application and Navigation Systems",
            "GROUND",
        ),

        (
            "04_Lesson 25. Cross-Country Planning, Fuel and Performance",
            "GROUND",
        ),

        (
            "05_Lesson 26. Dual Cross-Country I - Pilotage and Dead Reckoning",
            "GROUND + FLIGHT",
        ),

        (
            "06_Lesson 27. Dual Cross-Country II - Controlled Airports, Navigation Systems and Diversions",
            "GROUND + FLIGHT",
        ),

        (
            "07_Lesson 28. Basic Instrument Flight II - Navigation and ATC Services",
            "GROUND + FLIGHT",
        ),

        (
            "08_Lesson 29. Solo Cross-Country Readiness Check",
            "GROUND + FLIGHT · EVALUATION",
        ),

    ],


    "04_Stage IV. Night and Solo Cross-Country": [

        (
            "01_Lesson 30. Night Operations and Night Local Flight",
            "GROUND + FLIGHT",
        ),

        (
            "02_Lesson 31. Night Cross-Country",
            "GROUND + FLIGHT",
        ),

        (
            "03_Lesson 32. Solo Cross-Country I",
            "SOLO",
        ),

        (
            "04_Lesson 33. Long Solo Cross-Country",
            "SOLO",
        ),

        (
            "05_Lesson 34. Solo Cross-Country and Towered-Airport Experience",
            "SOLO",
        ),

    ],


    "05_Stage V. Certification Preparation": [

        (
            "01_Lesson 35. ACS Integration and Knowledge-Test Deficiencies",
            "GROUND",
        ),

        (
            "02_Lesson 36. Practical Test Preparation Flight",
            "GROUND + FLIGHT · EVALUATION",
        ),

        (
            "03_Lesson 37. Mock Oral and Scenario Cross-Country",
            "GROUND · EVALUATION",
        ),

        (
            "04_Lesson 38. Mock Practical Test",
            "GROUND + FLIGHT · EVALUATION",
        ),

        (
            "05_Lesson 39. Final Preparation, Requirements Audit and Endorsement",
            "GROUND · EVALUATION",
        ),

    ],

}


# =========================================================
# HELPERS
# =========================================================

def strip_prefix(name):

    if "_" in name:

        prefix, remainder = name.split(
            "_",
            1,
        )

        if prefix.isdigit():
            return remainder

    return name


def get_lesson_title(folder_name):

    clean_name = strip_prefix(
        folder_name
    )

    return clean_name


def build_template(
    lesson_name,
    lesson_type,
    stage_name,
):

    lesson_title = get_lesson_title(
        lesson_name
    )

    stage_title = strip_prefix(
        stage_name
    )

    has_flight = (
        "FLIGHT" in lesson_type
        or lesson_type == "SOLO"
    )

    markdown = f"""# {lesson_title}

## Lesson Information

- **Stage:** {stage_title}
- **Lesson Type:** {lesson_type}
- **Estimated Ground:** TBD
- **Estimated Flight:** TBD
- **Prerequisites:** TBD
- **Target Proficiency:** TBD

## Objective

TBD

## Completion Standards

TBD

## References

- TBD

## Regulatory and ACS Alignment

### Regulations

- TBD

### ACS

- TBD

## Why This Matters

TBD


# Prepare

## Before the Lesson

TBD

## Reading

- TBD

## Videos

- TBD

## Concepts to Understand

- TBD

## Study Check

TBD

[[answer:
TBD
]]


# Ground Brief

## Lesson Objective

TBD

## Completion Standards

TBD

## Introduction

### Attention

TBD

### Motivation

TBD

### Overview

TBD

## Knowledge

TBD

## Risk Management

TBD

## Skills and Procedures

TBD

## Scenario Application

TBD

## Review

TBD

## Instructor Evaluation

TBD

## Next Assignment

TBD
"""

    if has_flight:

        markdown += f"""

# Flight Card

## {lesson_title}

### Objectives

- TBD

### Sequence

- [ ] TBD
- [ ] TBD
- [ ] TBD

### Safety Priorities

1. Aircraft control
2. Collision avoidance
3. Situational awareness
4. Checklist discipline
5. Risk management

### Notes

TBD
"""

    markdown += """

# Debrief

## Learner Self-Assessment

### What went well?

____________________________________________________________

### What needs improvement?

____________________________________________________________

### What would you do differently next time?

____________________________________________________________

## Instructor Assessment

TBD

## Training Record

TBD

## Requirements Credited

TBD

## ACS Areas Trained

TBD

## Instructor Notes

____________________________________________________________

## Next Lesson

TBD
"""

    return markdown


# =========================================================
# BACKUP CURRENT PRIVATE SYLLABUS
# =========================================================

def backup_existing_private():

    if not PRIVATE_ROOT.exists():
        return None

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_root = (
        TRAINING_ROOT
        / f"private_backup_{timestamp}"
    )

    print()
    print(
        f"Backing up current Private syllabus:"
    )
    print(
        f"  {PRIVATE_ROOT}"
    )
    print(
        f"  -> {backup_root}"
    )

    shutil.move(
        str(PRIVATE_ROOT),
        str(backup_root),
    )

    return backup_root


# =========================================================
# CREATE NEW STRUCTURE
# =========================================================

def create_new_structure():

    PRIVATE_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    lesson_count = 0

    for stage_name, lessons in SYLLABUS.items():

        stage_path = (
            PRIVATE_ROOT
            / stage_name
        )

        stage_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        print()
        print(stage_name)

        for lesson_name, lesson_type in lessons:

            lesson_path = (
                stage_path
                / lesson_name
            )

            lesson_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            lesson_file = (
                lesson_path
                / "lesson.md"
            )

            lesson_file.write_text(
                build_template(
                    lesson_name,
                    lesson_type,
                    stage_name,
                ),
                encoding="utf-8",
            )

            print(
                f"  [CREATED] "
                f"{lesson_name} "
                f"[{lesson_type}]"
            )

            lesson_count += 1

    return lesson_count


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print(
        "PRIVATE PILOT SYLLABUS RESTRUCTURE"
    )
    print(
        "=================================="
    )

    backup_root = (
        backup_existing_private()
    )

    lesson_count = (
        create_new_structure()
    )

    print()
    print(
        "=================================="
    )
    print(
        f"Created {lesson_count} lessons."
    )

    if backup_root:

        print()
        print(
            "Previous syllabus preserved at:"
        )
        print(
            backup_root
        )

    print()
    print(
        "Restructure complete."
    )
    print()


if __name__ == "__main__":
    main()