from pathlib import Path
import shutil


PROJECT_ROOT = Path(__file__).resolve().parent
CFI_ROOT = PROJECT_ROOT / "content" / "cfi"


CFI_STRUCTURE = [

    (
        "01_Area I. Fundamentals of Instructing",
        [
            "01_Task A. Effects of Human Behavior and Communication on the Learning Process",
            "02_Task B. Learning Process",
            "03_Task C. Course Development, Lesson Plans, and Classroom Training Techniques",
            "04_Task D. Student Evaluation, Assessment, and Testing",
            "05_Task E. Elements of Effective Teaching in a Professional Environment",
            "06_Task F. Elements of Effective Teaching that Include Risk Management and Accident Prevention",
        ],
    ),

    (
        "02_Area II. Technical Subject Areas",
        [
            "01_Task A. Human Factors",
            "02_Task B. Visual Scanning and Collision Avoidance",
            "03_Task C. Runway Incursion Avoidance",
            "04_Task D. Principles of Flight",
            "05_Task E. Aircraft Flight Controls and Operation of Systems",
            "06_Task F. Performance and Limitations",
            "07_Task G. National Airspace System",
            "08_Task H. Navigation Systems and Radar Services",
            "09_Task I. Navigation and Cross-Country Flight Planning",
            "10_Task J. 14 CFR and Publications",
            "11_Task K. Endorsements and Logbook Entries",

            # Task L is seaplane only and intentionally omitted.

            "12_Task M. Night Operations",
            "13_Task N. High Altitude Operations - Supplemental Oxygen",
            "14_Task O. High Altitude Operations - Pressurization",

            # Task P is multiengine only and intentionally omitted.
        ],
    ),

    (
        "03_Area III. Preflight Preparation",
        [
            "01_Task A. Pilot Qualifications",
            "02_Task B. Airworthiness Requirements",
            "03_Task C. Weather Information",
        ],
    ),

    (
        "04_Area IV. Preflight Lesson on a Maneuver to be Performed in Flight",
        [
            "01_Task A. Maneuver Lesson",
        ],
    ),

    (
        "05_Area V. Preflight Procedures",
        [
            "01_Task A. Preflight Assessment",
            "02_Task B. Flight Deck Management",
            "03_Task C. Engine Starting",
            "04_Task D. Taxiing, Airport Signs, and Lighting",

            # Task E is seaplane only and intentionally omitted.

            "05_Task F. Before Takeoff Check",
        ],
    ),

    (
        "06_Area VI. Airport and Seaplane Base Operations",
        [
            "01_Task A. Communications, Light Signals, and Runway Lighting Systems",
            "02_Task B. Traffic Patterns",
        ],
    ),

    (
        "07_Area VII. Takeoffs, Landings, and Go-Arounds",
        [
            "01_Task A. Normal Takeoff and Climb",
            "02_Task B. Normal Approach and Landing",
            "03_Task C. Soft-Field Takeoff and Climb",
            "04_Task D. Soft-Field Approach and Landing",
            "05_Task E. Short-Field Takeoff and Maximum Performance Climb",
            "06_Task F. Short-Field Approach and Landing",

            # Tasks G-L are seaplane only and intentionally omitted.

            "07_Task M. Slip to a Landing",

            # "/" cannot be used in a Windows folder name.
            # The lesson title itself will use the exact ACS wording:
            # Task N. Go-Around/Rejected Landing
            "08_Task N. Go-Around-Rejected Landing",

            "09_Task O. Power-Off 180° Accuracy Approach and Landing",
        ],
    ),

    (
        "08_Area VIII. Fundamentals of Flight",
        [
            "01_Task A. Straight-and-Level Flight",
            "02_Task B. Level Turns",
            "03_Task C. Straight Climbs and Climbing Turns",
            "04_Task D. Straight Descents and Descending Turns",
        ],
    ),

    (
        "09_Area IX. Performance and Ground Reference Maneuvers",
        [
            "01_Task A. Steep Turns",
            "02_Task B. Steep Spiral",
            "03_Task C. Chandelles",
            "04_Task D. Lazy Eights",

            # Rectangular Course, S-Turns, and Turns Around a Point
            # are elements of this ACS Task, not separate Tasks.
            "05_Task E. Ground Reference Maneuvers",

            "06_Task F. Eights on Pylons",
        ],
    ),

    (
        "10_Area X. Slow flight, Stalls, and Spins",
        [
            "01_Task A. Maneuvering During Slow Flight",
            "02_Task B. Demonstration of Flight Characteristics at Various Configurations and Airspeeds",
            "03_Task C. Power-Off Stalls",
            "04_Task D. Power-On Stalls",
            "05_Task E. Accelerated Stalls",
            "06_Task F. Cross-Controlled Stall Demonstration",
            "07_Task G. Elevator Trim Stall Demonstration",
            "08_Task H. Secondary Stall Demonstration",
            "09_Task I. Spin Awareness and Spins",
        ],
    ),

    (
        "11_Area XI. Basic Instrument Maneuvers",
        [
            "01_Task A. Straight-and-Level Flight",
            "02_Task B. Constant Airspeed Climbs",
            "03_Task C. Constant Airspeed Descents",
            "04_Task D. Turns to Headings",
            "05_Task E. Recovery from Unusual Flight Attitudes",
        ],
    ),

    (
        "12_Area XII. Emergency Operations",
        [
            "01_Task A. Emergency Descent",
            "02_Task B. Emergency Approach and Landing (Simulated)",
            "03_Task C. Systems and Equipment Malfunctions",
            "04_Task D. Emergency Equipment and Survival Gear",

            # Tasks E-G are multiengine only and intentionally omitted.
        ],
    ),

    # Area XIII. Multiengine Operations intentionally omitted
    # from the ASEL lesson-plan library.

    (
        "14_Area XIV. Postflight Procedures",
        [
            "01_Task A. After Landing, Parking, and Securing",

            # Task B is seaplane only and intentionally omitted.
        ],
    ),
]


def ensure_safe_to_rebuild():

    if not CFI_ROOT.exists():
        return

    existing_files = [
        path
        for path in CFI_ROOT.rglob("*")
        if path.is_file()
    ]

    if existing_files:

        print()
        print("STOPPED")
        print("=" * 60)
        print(
            "Files already exist inside content/cfi."
        )
        print(
            "The script will not delete existing lesson content."
        )
        print()

        for path in existing_files:
            print(
                path.relative_to(CFI_ROOT)
            )

        raise RuntimeError(
            "CFI library contains files. "
            "Rebuild cancelled to prevent data loss."
        )


def create_structure():

    if CFI_ROOT.exists():

        print(
            "Removing existing empty CFI folder structure..."
        )

        shutil.rmtree(
            CFI_ROOT
        )


    CFI_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )


    task_count = 0
    area_count = 0


    for area_name, tasks in CFI_STRUCTURE:

        area_path = (
            CFI_ROOT
            / area_name
        )

        area_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        area_count += 1

        print()
        print(
            area_name
        )


        for task_name in tasks:

            task_path = (
                area_path
                / task_name
            )

            task_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            assets_path = (
                task_path
                / "assets"
            )

            assets_path.mkdir(
                exist_ok=True,
            )

            print(
                f"  {task_name}"
            )

            task_count += 1


    print()
    print("=" * 60)
    print("CFI ASEL FOLDER BUILD COMPLETE")
    print("=" * 60)

    print(
        f"Areas: {area_count}"
    )

    print(
        f"Tasks: {task_count}"
    )

    print(
        f"Location: {CFI_ROOT.resolve()}"
    )


def main():

    ensure_safe_to_rebuild()

    create_structure()


if __name__ == "__main__":
    main()