document.addEventListener(
    "DOMContentLoaded",
    function () {

        const lesson =
            document.querySelector(
                ".training-lesson"
            );

        if (!lesson) {
            return;
        }


        // =================================================
        // SECTION NAVIGATION
        // =================================================

        const tabs =
            document.querySelectorAll(
                "[data-lesson-tab]"
            );

        const panels =
            document.querySelectorAll(
                "[data-lesson-panel]"
            );


        function showSection(sectionName) {

            tabs.forEach(
                function (tab) {

                    const active =
                        tab.dataset.lessonTab
                        === sectionName;

                    tab.classList.toggle(
                        "active",
                        active
                    );

                    tab.setAttribute(
                        "aria-selected",
                        active
                            ? "true"
                            : "false"
                    );

                }
            );


            panels.forEach(
                function (panel) {

                    const active =
                        panel.dataset.lessonPanel
                        === sectionName;

                    panel.hidden =
                        !active;

                    panel.classList.toggle(
                        "active",
                        active
                    );

                }
            );


            history.replaceState(
                null,
                "",
                "#" + sectionName
            );

            window.scrollTo({
                top: 0,
                behavior: "instant",
            });

        }


        tabs.forEach(
            function (tab) {

                tab.addEventListener(
                    "click",
                    function () {

                        showSection(
                            tab.dataset.lessonTab
                        );

                    }
                );

            }
        );


        // Allow direct links:
        //
        // /lesson-url#prepare
        // /lesson-url#brief
        // /lesson-url#fly
        // /lesson-url#debrief

        const initialSection =
            window.location.hash
            .replace("#", "");

        const validSections =
            Array.from(tabs).map(
                function (tab) {

                    return tab.dataset.lessonTab;

                }
            );

        if (
            validSections.includes(
                initialSection
            )
        ) {

            showSection(
                initialSection
            );

        }


        // =================================================
        // PRINT HELPERS
        // =================================================

        function installPageStyle(
            size,
            margin
        ) {

            const oldStyle =
                document.getElementById(
                    "dynamic-print-page-style"
                );

            if (oldStyle) {
                oldStyle.remove();
            }

            const style =
                document.createElement(
                    "style"
                );

            style.id =
                "dynamic-print-page-style";

            style.textContent = `
                @page {
                    size: ${size};
                    margin: ${margin};
                }
            `;

            document.head.appendChild(
                style
            );

        }


        function removePageStyle() {

            const style =
                document.getElementById(
                    "dynamic-print-page-style"
                );

            if (style) {
                style.remove();
            }

        }


        window.addEventListener(
            "afterprint",
            function () {

                document.body.classList.remove(
                    "print-kneeboard",
                    "print-debrief"
                );

                removePageStyle();

            }
        );


        // =================================================
        // KNEEBOARD
        // =================================================

        const kneeboardButton =
            document.getElementById(
                "save-kneeboard"
            );

        if (kneeboardButton) {

            kneeboardButton.addEventListener(
                "click",
                function () {

                    document.body.classList.add(
                        "print-kneeboard"
                    );

                    installPageStyle(
                        "11in 8.5in",
                        "0"
                    );

                    window.print();

                }
            );

        }


        // =================================================
        // DEBRIEF LOCAL STORAGE
        // =================================================

        const lessonPath =
            lesson.dataset.lessonPath;

        const lessonTitle =
            lesson.dataset.lessonTitle;

        const storageKey =
            "flight-guide-debrief:"
            + lessonPath;


        const debriefFields =
            document.querySelectorAll(
                "[data-debrief-field]"
            );


        function getDebriefData() {

            const data = {};

            debriefFields.forEach(
                function (field) {

                    data[
                        field.dataset.debriefField
                    ] = field.value;

                }
            );

            return data;

        }


        function saveDraft() {

            const data =
                getDebriefData();

            localStorage.setItem(
                storageKey,
                JSON.stringify(data)
            );

        }


        function loadDraft() {

            const raw =
                localStorage.getItem(
                    storageKey
                );

            if (!raw) {
                return;
            }

            try {

                const data =
                    JSON.parse(raw);

                debriefFields.forEach(
                    function (field) {

                        const key =
                            field.dataset
                            .debriefField;

                        if (
                            data[key] !==
                            undefined
                        ) {

                            field.value =
                                data[key];

                        }

                    }
                );

            } catch (error) {

                console.warn(
                    "Unable to load debrief draft.",
                    error
                );

            }

        }


        debriefFields.forEach(
            function (field) {

                field.addEventListener(
                    "input",
                    saveDraft
                );

                field.addEventListener(
                    "change",
                    saveDraft
                );

            }
        );


        loadDraft();


        // Set today's date automatically
        // if the field is still blank.

        const dateField =
            document.querySelector(
                '[data-debrief-field="date"]'
            );

        if (
            dateField
            && !dateField.value
        ) {

            const today =
                new Date();

            const localDate =
                new Date(
                    today.getTime()
                    - today.getTimezoneOffset()
                    * 60000
                )
                .toISOString()
                .slice(0, 10);

            dateField.value =
                localDate;

            saveDraft();

        }


        // =================================================
        // DOWNLOAD DEBRIEF AS MARKDOWN
        // =================================================

        function safeFilename(value) {

            return value
                .replace(
                    /[^a-z0-9]+/gi,
                    "_"
                )
                .replace(
                    /^_+|_+$/g,
                    ""
                );

        }


        function markdownValue(value) {

            if (!value) {
                return "";
            }

            return value.trim();
        }


        const saveDebriefButton =
            document.getElementById(
                "save-debrief"
            );

        if (saveDebriefButton) {

            saveDebriefButton.addEventListener(
                "click",
                function () {

                    const data =
                        getDebriefData();

                    const markdown = `
# Flight Guide Debrief

## Lesson

${lessonTitle}

## Record

- **Student / Pilot:** ${markdownValue(data.student)}
- **Instructor:** ${markdownValue(data.instructor)}
- **Date:** ${markdownValue(data.date)}
- **Aircraft / N-Number:** ${markdownValue(data.aircraft)}
- **Flight Time:** ${markdownValue(data.flight_time)}

## What Went Well

${markdownValue(data.went_well)}

## What Needs Improvement

${markdownValue(data.needs_improvement)}

## Instructor Notes

${markdownValue(data.instructor_notes)}

## Next Assignment / Lesson

${markdownValue(data.next_assignment)}
`.trim();


                    const blob =
                        new Blob(
                            [markdown],
                            {
                                type:
                                    "text/markdown;charset=utf-8"
                            }
                        );


                    const url =
                        URL.createObjectURL(
                            blob
                        );


                    const anchor =
                        document.createElement(
                            "a"
                        );

                    const datePart =
                        data.date
                        || "undated";

                    anchor.href =
                        url;

                    anchor.download =
                        safeFilename(
                            lessonTitle
                        )
                        + "_Debrief_"
                        + datePart
                        + ".md";


                    document.body.appendChild(
                        anchor
                    );

                    anchor.click();

                    anchor.remove();

                    URL.revokeObjectURL(
                        url
                    );

                }
            );

        }


        // =================================================
        // PRINT DEBRIEF
        // =================================================

        const printDebriefButton =
            document.getElementById(
                "print-debrief"
            );

        if (printDebriefButton) {

            printDebriefButton.addEventListener(
                "click",
                function () {

                    document.body.classList.add(
                        "print-debrief"
                    );

                    installPageStyle(
                        "letter portrait",
                        "0.5in"
                    );

                    window.print();

                }
            );

        }

    }
);