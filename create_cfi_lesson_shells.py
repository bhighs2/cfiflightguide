from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent
CFI_ROOT = PROJECT_ROOT / "content" / "cfi"


def clean_folder_name(name):
    """
    Remove the numeric ordering prefix.

    Example:

    01_Area I. Fundamentals of Instructing

    becomes:

    Area I. Fundamentals of Instructing
    """

    return re.sub(
        r"^\d+_",
        "",
        name,
    )


def build_lesson_template(
    area_name,
    task_name,
):
    """
    Return the standard CFI lesson-plan Markdown shell.
    """

    return f"""# {task_name}

## Area of Operation

{area_name}

## Objective



## References



## Teaching Aids / Equipment



## ACS Elements

### Knowledge



### Risk Management



### Skills



## Lesson Presentation

### Purpose



### Key Teaching Points



### Application



### Risk Management and Safety



### Procedure / Technique



### Demonstration and Learner Practice



## Common Errors



## Scenario



## Review and Assessment

### Questions



### Scenario Questions



## Completion Standards


"""


def main():

    if not CFI_ROOT.exists():

        raise RuntimeError(
            f"CFI folder does not exist: "
            f"{CFI_ROOT.resolve()}"
        )


    created = 0
    existing = 0


    area_folders = sorted(
        [
            path
            for path in CFI_ROOT.iterdir()
            if path.is_dir()
        ]
    )


    for area_path in area_folders:

        area_name = clean_folder_name(
            area_path.name
        )


        task_folders = sorted(
            [
                path
                for path in area_path.iterdir()
                if (
                    path.is_dir()
                    and clean_folder_name(
                        path.name
                    ).startswith("Task ")
                )
            ]
        )


        for task_path in task_folders:

            task_name = clean_folder_name(
                task_path.name
            )


            # Make sure every Task has an assets folder.

            assets_path = (
                task_path
                / "assets"
            )

            assets_path.mkdir(
                exist_ok=True
            )


            lesson_path = (
                task_path
                / "lesson.md"
            )


            # Never overwrite authored lesson content.

            if lesson_path.exists():

                print(
                    f"EXISTS: "
                    f"{area_name} → {task_name}"
                )

                existing += 1
                continue


            lesson_content = (
                build_lesson_template(
                    area_name,
                    task_name,
                )
            )


            lesson_path.write_text(
                lesson_content,
                encoding="utf-8",
            )


            print(
                f"CREATED: "
                f"{area_name} → {task_name}"
            )

            created += 1


    print()
    print("=" * 60)
    print("CFI LESSON SHELL BUILD COMPLETE")
    print("=" * 60)

    print(
        f"Created: {created}"
    )

    print(
        f"Already existed: {existing}"
    )

    print(
        f"Location: {CFI_ROOT.resolve()}"
    )


if __name__ == "__main__":
    main()