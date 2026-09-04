from pathlib import Path


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

PRIVATE_SYLLABUS_ROOT = (
    PROJECT_ROOT
    / "content"
    / "training_syllabi"
    / "private"
)


# =========================================================
# PRIVATE PILOT TRAINING SYLLABUS
# =========================================================

SYLLABUS = {
    "00_Stage 0. Course Orientation": [
        "00_Lesson 0. Course Orientation and Training Expectations",
    ],

    "01_Stage I. Pre-Solo": [
        "01_Lesson 1. Aircraft Familiarization and Basic Control",
        "02_Lesson 2. Traffic Pattern and Landing Introduction",
        "03_Lesson 3. Slow Flight and Stalls",
        "04_Lesson 4. Wind Correction and Ground Reference Maneuvers",
        "05_Lesson 5. Emergencies, Slips, and Engine-Failure Approaches",
        "06_Lesson 6. Crosswind Operations and Landing Refinement",
        "07_Lesson 7. Pre-Solo Review and Evaluation",
        "08_Lesson 8. First Solo",
    ],

    "02_Stage II. Post-Solo Proficiency": [
        "01_Lesson 9. Local Solo Consolidation",
        "02_Lesson 10. Steep Turns and Precision Aircraft Control",
        "03_Lesson 11. Short-Field and Soft-Field Operations",
        "04_Lesson 12. Emergency Operations and Systems Malfunctions",
        "05_Lesson 13. Basic Instrument Flight I",
        "06_Lesson 14. Local Solo Proficiency",
    ],

    "03_Stage III. Cross-Country": [
        "01_Lesson 15. Cross-Country Planning",
        "02_Lesson 16. Dual Cross-Country I",
        "03_Lesson 17. Dual Cross-Country II",
        "04_Lesson 18. Basic Instrument Flight II",
        "05_Lesson 19. Solo Cross-Country Readiness",
    ],

    "04_Stage IV. Night and Solo Cross-Country": [
        "01_Lesson 20. Night Local Operations",
        "02_Lesson 21. Night Cross-Country",
        "03_Lesson 22. Solo Cross-Country I",
        "04_Lesson 23. Long Solo Cross-Country",
        "05_Lesson 24. Solo Cross-Country and Experience Builder",
    ],

    "05_Stage V. Certification Preparation": [
        "01_Lesson 25. ACS Integration and Knowledge Test Review",
        "02_Lesson 26. Practical Test Preparation Flight I",
        "03_Lesson 27. Mock Oral and Scenario Cross-Country",
        "04_Lesson 28. Mock Practical Test",
        "05_Lesson 29. Final Preparation and Endorsement",
    ],
}


# =========================================================
# CREATE FOLDERS
# =========================================================

def main():
    PRIVATE_SYLLABUS_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    created_count = 0
    existing_count = 0

    print()
    print("Creating Private Pilot training syllabus...")
    print(f"Root: {PRIVATE_SYLLABUS_ROOT}")
    print()

    for stage_name, lessons in SYLLABUS.items():

        stage_path = (
            PRIVATE_SYLLABUS_ROOT
            / stage_name
        )

        if stage_path.exists():
            existing_count += 1
            print(f"[EXISTS]  {stage_name}")
        else:
            stage_path.mkdir(
                parents=True,
                exist_ok=True,
            )
            created_count += 1
            print(f"[CREATED] {stage_name}")

        for lesson_name in lessons:

            lesson_path = (
                stage_path
                / lesson_name
            )

            if lesson_path.exists():
                existing_count += 1
                print(
                    f"    [EXISTS]  {lesson_name}"
                )

            else:
                lesson_path.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                created_count += 1

                print(
                    f"    [CREATED] {lesson_name}"
                )

    print()
    print("----------------------------------------")
    print("Private syllabus folder creation complete.")
    print(f"Created: {created_count}")
    print(f"Already existed: {existing_count}")
    print("----------------------------------------")
    print()


if __name__ == "__main__":
    main()