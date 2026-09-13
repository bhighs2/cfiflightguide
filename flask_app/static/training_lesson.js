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


        const isCfiAcsLesson =
            lesson.classList.contains(
                "cfi-acs-lesson"
            );


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
                    "print-debrief",
                    "print-cfi-lesson",
                    "print-instructor-notes"
                );

                const printArea =
                    document.getElementById(
                        "cfi-lesson-print-area"
                    );

                if (printArea) {
                    printArea.remove();
                }

                const instructorNotesPrintArea =
                    document.getElementById(
                        "instructor-notes-print-area"
                    );

                if (instructorNotesPrintArea) {
                    instructorNotesPrintArea.remove();
                }

                removePageStyle();

            }
        );


        // =================================================
        // CFI ACS LESSON
        // =================================================

        function revealPrintableContent(
            content
        ) {

            content.querySelectorAll(
                ".lesson-section"
            ).forEach(
                function (section) {

                    section.classList.remove(
                        "collapsed"
                    );

                    const body =
                        section.querySelector(
                            ".lesson-section-body"
                        );

                    if (body) {
                        body.hidden = false;
                    }

                }
            );

            content.querySelectorAll(
                ".lesson-part"
            ).forEach(
                function (part) {

                    part.classList.remove(
                        "collapsed"
                    );

                    const body =
                        part.querySelector(
                            ".lesson-part-body"
                        );

                    if (body) {
                        body.hidden = false;
                    }

                }
            );

            content.querySelectorAll(
                "details"
            ).forEach(
                function (details) {

                    details.open = true;

                }
            );

        }


        function replacePrintToggle(
            button
        ) {

            const title =
                button.querySelector(
                    ".lesson-section-title, .lesson-part-title"
                );

            const replacement =
                document.createElement(
                    "span"
                );

            replacement.className =
                "cfi-print-section-title";

            replacement.innerHTML = title
                ? title.innerHTML
                : button.innerHTML;

            button.replaceWith(
                replacement
            );

        }


        function groupCfiPrintSubsections(
            content
        ) {

            content.querySelectorAll(
                ".lesson-section-body"
            ).forEach(
                function (sectionBody) {

                    Array.from(
                        sectionBody.children
                    ).filter(
                        function (element) {

                            return (
                                element.tagName === "H3"
                            );

                        }
                    ).forEach(
                        function (heading) {

                            const subsection =
                                document.createElement(
                                    "section"
                                );

                            subsection.className =
                                "cfi-print-subsection";

                            sectionBody.insertBefore(
                                subsection,
                                heading
                            );

                            subsection.appendChild(
                                heading
                            );

                            while (
                                subsection.nextSibling
                            ) {

                                const next =
                                    subsection.nextSibling;

                                if (
                                    next.nodeType
                                    === Node.ELEMENT_NODE
                                    && next.tagName === "H3"
                                ) {
                                    break;
                                }

                                subsection.appendChild(
                                    next
                                );

                            }

                        }
                    );

                }
            );

        }


        function sanitizeCfiPrintContent(
            content
        ) {

            revealPrintableContent(
                content
            );

            groupCfiPrintSubsections(
                content
            );

            content.querySelectorAll(
                ".lesson-section-toggle, .lesson-part-toggle"
            ).forEach(
                replacePrintToggle
            );

            content.querySelectorAll(
                ".youtube-embed, .youtube-segment"
            ).forEach(
                function (element) {

                    element.remove();

                }
            );

            content.querySelectorAll(
                ".pdf-embed"
            ).forEach(
                function (element) {

                    const viewer =
                        element.querySelector(
                            ".pdf-viewer"
                        );

                    if (viewer) {
                        viewer.remove();
                    }

                    const toggle =
                        element.querySelector(
                            ".pdf-source-toggle"
                        );

                    if (toggle) {
                        const staticToggle =
                            document.createElement(
                                "div"
                            );

                        staticToggle.className =
                            "pdf-source-toggle";

                        staticToggle.innerHTML =
                            toggle.innerHTML;

                        const action =
                            staticToggle.querySelector(
                                ".pdf-source-action"
                            );

                        if (action) {
                            action.remove();
                        }

                        element.replaceWith(
                            staticToggle
                        );
                    } else {
                        element.remove();
                    }

                }
            );

            content.querySelectorAll(
                'input[type="checkbox"]'
            ).forEach(
                function (checkbox) {

                    const printCheckbox =
                        document.createElement(
                            "span"
                        );

                    printCheckbox.className =
                        "cfi-print-checkbox";

                    printCheckbox.setAttribute(
                        "aria-hidden",
                        "true"
                    );

                    checkbox.replaceWith(
                        printCheckbox
                    );

                }
            );

            content.querySelectorAll(
                "p"
            ).forEach(
                function (paragraph) {

                    const text =
                        paragraph.textContent
                            .replace(/\s+/g, " ")
                            .trim();

                    if (
                        /^Source:?$/i.test(text)
                        || /^SOURCE:?$/i.test(text)
                    ) {
                        paragraph.remove();
                    }

                }
            );

            content.querySelectorAll(
                ".pdf-source-toggle"
            ).forEach(
                function (element) {

                    const replacement =
                        document.createElement(
                            "div"
                        );

                    replacement.className =
                        "pdf-source-toggle";

                    replacement.setAttribute(
                        "aria-hidden",
                        "true"
                    );

                    replacement.innerHTML =
                        element.innerHTML;

                    element.replaceWith(
                        replacement
                    );

                }
            );

            content.querySelectorAll(
                "button, input, select, textarea, iframe, video, audio"
            ).forEach(
                function (element) {

                    element.remove();

                }
            );

        }


        function waitForPrintImages(
            printArea
        ) {

            const imageLoads = Array.from(
                printArea.querySelectorAll(
                    "img"
                )
            ).map(
                function (image) {

                    image.loading = "eager";

                    if (image.complete) {
                        return Promise.resolve();
                    }

                    return new Promise(
                        function (resolve) {

                            image.addEventListener(
                                "load",
                                resolve,
                                { once: true }
                            );

                            image.addEventListener(
                                "error",
                                resolve,
                                { once: true }
                            );

                        }
                    );

                }
            );

            return Promise.all(imageLoads);

        }


        const printInstructorNotesButtons =
            document.querySelectorAll(
                "[data-print-instructor-notes]"
            );

        if (
            isCfiAcsLesson
            && printInstructorNotesButtons.length
        ) {

            printInstructorNotesButtons.forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            const notesSection =
                                button.closest(
                                    ".lesson-section"
                                );

                            if (!notesSection) {
                                return;
                            }

                            const oldPrintArea =
                                document.getElementById(
                                    "instructor-notes-print-area"
                                );

                            if (oldPrintArea) {
                                oldPrintArea.remove();
                            }

                            const printArea =
                                document.createElement(
                                    "section"
                                );

                            printArea.id =
                                "instructor-notes-print-area";

                            const printHeader =
                                document.createElement(
                                    "header"
                                );

                            printHeader.className =
                                "instructor-notes-print-header";

                            const areaHeading =
                                document.createElement(
                                    "div"
                                );

                            areaHeading.className =
                                "instructor-notes-print-area-title";

                            areaHeading.textContent =
                                lesson.dataset.areaTitle;

                            const taskHeading =
                                document.createElement(
                                    "div"
                                );

                            taskHeading.className =
                                "instructor-notes-print-task-title";

                            taskHeading.textContent =
                                lessonTitle;

                            printHeader.append(
                                areaHeading,
                                taskHeading
                            );

                            printArea.appendChild(
                                printHeader
                            );

                            const clone =
                                notesSection.cloneNode(true);

                            clone.querySelectorAll(
                                ".instructor-notes-toolbar"
                            ).forEach(
                                function (toolbar) {

                                    toolbar.remove();

                                }
                            );

                            const notesBody =
                                clone.querySelector(
                                    ".lesson-section-body"
                                );

                            if (notesBody) {

                                const sectionHeadings =
                                    Array.from(
                                        notesBody.children
                                    ).filter(
                                        function (element) {

                                            return (
                                                element.tagName === "H3"
                                            );

                                        }
                                    );

                                if (sectionHeadings.length) {

                                    sectionHeadings.forEach(
                                        function (sectionHeading) {

                                            const pair =
                                                document.createElement(
                                                    "div"
                                                );

                                            pair.className =
                                                "instructor-notes-print-pair";

                                            notesBody.insertBefore(
                                                pair,
                                                sectionHeading
                                            );

                                            pair.appendChild(
                                                sectionHeading
                                            );

                                            while (
                                                pair.nextElementSibling
                                                && pair.nextElementSibling.tagName
                                                    !== "H3"
                                            ) {

                                                pair.appendChild(
                                                    pair.nextElementSibling
                                                );

                                            }

                                        }
                                    );

                                } else {

                                    Array.from(
                                        notesBody.children
                                    ).filter(
                                        function (element) {

                                            const text =
                                                element.textContent.trim();

                                            return (
                                                element.tagName === "P"
                                                && /^\d+\./.test(text)
                                            ) || (
                                                element.tagName === "UL"
                                                && /^\d+\./.test(text)
                                            ) || (
                                                element.tagName === "OL"
                                            );

                                        }
                                    ).forEach(
                                        function (lectureItem) {

                                            const pair =
                                                document.createElement(
                                                    "div"
                                                );

                                            pair.className =
                                                "instructor-notes-print-pair";

                                            notesBody.insertBefore(
                                                pair,
                                                lectureItem
                                            );

                                            pair.appendChild(
                                                lectureItem
                                            );

                                            const memoryAid =
                                                pair.nextElementSibling;

                                            if (
                                                memoryAid
                                                && memoryAid.classList.contains(
                                                    "lesson-mnemonic"
                                                )
                                            ) {

                                                pair.appendChild(
                                                    memoryAid
                                                );

                                            }

                                        }
                                    );

                                }

                            }

                            sanitizeCfiPrintContent(
                                clone
                            );

                            printArea.appendChild(
                                clone
                            );

                            lesson.appendChild(
                                printArea
                            );

                            document.body.classList.add(
                                "print-instructor-notes"
                            );

                            installPageStyle(
                                "letter portrait",
                                "0.3in"
                            );

                            waitForPrintImages(
                                printArea
                            ).then(
                                function () {

                                    window.print();

                                }
                            );

                        }
                    );

                }
            );

        }


        const printCfiLessonButton =
            document.getElementById(
                "print-cfi-lesson"
            );

        if (
            isCfiAcsLesson
            && printCfiLessonButton
        ) {

            printCfiLessonButton.addEventListener(
                "click",
                function () {

                    const oldPrintArea =
                        document.getElementById(
                            "cfi-lesson-print-area"
                        );

                    if (oldPrintArea) {
                        oldPrintArea.remove();
                    }

                    const printArea =
                        document.createElement(
                            "section"
                        );

                    printArea.id =
                        "cfi-lesson-print-area";

                    ["overview", "teach", "fly"]
                    .forEach(
                        function (sectionName) {

                            const panel =
                                document.querySelector(
                                    '[data-lesson-panel="'
                                    + sectionName
                                    + '"]'
                                );

                            if (!panel) {
                                return;
                            }

                            const content =
                                panel.querySelector(
                                    ".markdown-content"
                                );

                            if (!content) {
                                return;
                            }

                            const clone =
                                content.cloneNode(true);

                            if (
                                sectionName === "fly"
                            ) {

                                const kneeboard =
                                    clone.querySelector(
                                        ".kneeboard-section"
                                    );

                                if (kneeboard) {
                                    kneeboard.remove();
                                }

                            }

                            clone.classList.add(
                                "cfi-print-panel"
                            );

                            sanitizeCfiPrintContent(
                                clone
                            );

                            printArea.appendChild(
                                clone
                            );

                        }
                    );

                    if (!printArea.children.length) {
                        return;
                    }

                    lesson.appendChild(
                        printArea
                    );

                    document.body.classList.add(
                        "print-cfi-lesson"
                    );

                    installPageStyle(
                        "letter portrait",
                        "0.35in"
                    );

                    waitForPrintImages(
                        printArea
                    ).then(
                        function () {

                            window.print();

                        }
                    );

                }
            );

        }


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