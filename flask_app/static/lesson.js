document.addEventListener(
    "DOMContentLoaded",
    function () {

        /* =============================================
           LESSON CONTENT ROOTS
        ============================================= */

        const contents =
            document.querySelectorAll(
                ".markdown-content"
            );

        if (contents.length === 0) {
            return;
        }


        /*
         * Standard / ACS lessons historically use one
         * Markdown content root. Keep a reference to the
         * first root for the legacy ACS part-navigation
         * logic farther down this file.
         */

        const content =
            contents[0];


        const isTrainingLesson =
            document.querySelector(
                ".training-lesson"
            ) !== null;


        function setLessonSectionState(
            section,
            collapsed
        ) {

            const body =
                section.querySelector(
                    ".lesson-section-body"
                );

            const button =
                section.querySelector(
                    ".lesson-section-toggle"
                );


            section.classList.toggle(
                "collapsed",
                collapsed
            );


            if (body) {

                body.hidden =
                    collapsed;

            }


            if (button) {

                button.setAttribute(
                    "aria-expanded",
                    collapsed
                        ? "false"
                        : "true"
                );

            }

        }


        /* =============================================
           MAJOR H2 SECTIONS
        ============================================= */

        function initializeLessonSections(
            content,
            useAccordion
        ) {

            const headings =
                Array.from(
                    content.children
                ).filter(
                    function (element) {

                        return (
                            element.tagName
                            === "H2"
                        );

                    }
                );


            headings.forEach(
                function (
                    heading,
                    index
                ) {

                    const section =
                        document.createElement(
                            "section"
                        );

                    section.className =
                        "lesson-section";


                    const body =
                        document.createElement(
                            "div"
                        );

                    body.className =
                        "lesson-section-body";


                    content.insertBefore(
                        section,
                        heading
                    );


                    section.appendChild(
                        heading
                    );

                    section.appendChild(
                        body
                    );


                    while (
                        section.nextSibling
                    ) {

                        const next =
                            section.nextSibling;


                        if (
                            next.nodeType
                            === Node.ELEMENT_NODE
                            &&
                            (
                                next.tagName === "H2"
                                ||
                                next.tagName === "H1"
                            )
                        ) {

                            break;

                        }


                        body.appendChild(
                            next
                        );

                    }


                    const headingHtml =
                        heading.innerHTML;


                    heading.innerHTML = "";

                    heading.classList.add(
                        "lesson-section-heading"
                    );


                    const button =
                        document.createElement(
                            "button"
                        );

                    button.type =
                        "button";

                    button.className =
                        "lesson-section-toggle";


                    const title =
                        document.createElement(
                            "span"
                        );

                    title.className =
                        "lesson-section-title";

                    title.innerHTML =
                        headingHtml;


                    const chevron =
                        document.createElement(
                            "span"
                        );

                    chevron.className =
                        "lesson-section-chevron";

                    chevron.setAttribute(
                        "aria-hidden",
                        "true"
                    );

                    chevron.textContent =
                        "›";


                    button.appendChild(
                        title
                    );

                    button.appendChild(
                        chevron
                    );

                    heading.appendChild(
                        button
                    );


                    /*
                     * Training syllabus behavior:
                     *
                     * First H2 open.
                     * Every other H2 closed.
                     */

                    const shouldCollapse =
                        useAccordion
                        && index > 0;


                    setLessonSectionState(
                        section,
                        shouldCollapse
                    );


                    button.addEventListener(
                        "click",
                        function () {

                            const currentlyCollapsed =
                                section.classList.contains(
                                    "collapsed"
                                );


                            /*
                             * If opening a section in a
                             * training lesson, close its
                             * sibling H2 sections first.
                             */

                            if (
                                useAccordion
                                && currentlyCollapsed
                            ) {

                                Array.from(
                                    content.children
                                ).forEach(
                                    function (
                                        otherSection
                                    ) {

                                        if (
                                            otherSection
                                            !== section
                                            &&
                                            otherSection
                                            .classList
                                            .contains(
                                                "lesson-section"
                                            )
                                        ) {

                                            setLessonSectionState(
                                                otherSection,
                                                true
                                            );

                                        }

                                    }
                                );

                            }


                            setLessonSectionState(
                                section,
                                !currentlyCollapsed
                            );

                        }
                    );

                }
            );

        }


        /* =============================================
           H3 SUBSECTIONS
        ============================================= */

        function initializeLessonSubsections(
            content
        ) {

            const sectionBodies =
                content.querySelectorAll(
                    ".lesson-section-body"
                );


            sectionBodies.forEach(
                function (
                    sectionBody
                ) {

                    const headings =
                        Array.from(
                            sectionBody.children
                        ).filter(
                            function (
                                element
                            ) {

                                return (
                                    element.tagName
                                    === "H3"
                                );

                            }
                        );


                    headings.forEach(
                        function (
                            heading
                        ) {

                            const subsection =
                                document.createElement(
                                    "section"
                                );

                            subsection.className =
                                "lesson-subsection";


                            const body =
                                document.createElement(
                                    "div"
                                );

                            body.className =
                                "lesson-subsection-body";


                            sectionBody.insertBefore(
                                subsection,
                                heading
                            );


                            subsection.appendChild(
                                heading
                            );

                            subsection.appendChild(
                                body
                            );


                            /*
                             * Everything after this H3
                             * belongs to it until the
                             * next H3.
                             */

                            while (
                                subsection.nextSibling
                            ) {

                                const next =
                                    subsection.nextSibling;


                                if (
                                    next.nodeType
                                    === Node.ELEMENT_NODE
                                    &&
                                    next.tagName
                                    === "H3"
                                ) {

                                    break;

                                }


                                body.appendChild(
                                    next
                                );

                            }


                            heading.classList.add(
                                "lesson-subsection-heading"
                            );

                        }
                    );

                }
            );

        }


        /* =============================================
           INITIALIZE EACH MARKDOWN PANEL
        ============================================= */

        contents.forEach(
            function (
                content
            ) {

                const panel =
                    content.closest(
                        "[data-lesson-panel]"
                    );


                const panelName =
                    panel
                        ? panel.dataset.lessonPanel
                        : null;


                initializeLessonSections(
                    content,
                    isTrainingLesson
                );


                /*
                 * Brief and Fly both use the deeper
                 * H3 subsection-card hierarchy.
                 */

                if (
                    isTrainingLesson
                    &&
                    (
                        panelName === "brief"
                        ||
                        panelName === "fly"
                    )
                ) {

                    initializeLessonSubsections(
                        content
                    );

                }


                /*
                 * In the Fly panel, identify the
                 * intentionally abbreviated Kneeboard
                 * H2 section so print CSS can show
                 * only that section.
                 */

                if (
                    isTrainingLesson
                    && panelName === "fly"
                ) {

                    const sections =
                        content.querySelectorAll(
                            ".lesson-section"
                        );


                    sections.forEach(
                        function (
                            section
                        ) {

                            const title =
                                section.querySelector(
                                    ".lesson-section-title"
                                );


                            if (
                                title
                                &&
                                title.textContent
                                .trim()
                                .toLowerCase()
                                === "kneeboard"
                            ) {

                                section.classList.add(
                                    "kneeboard-section"
                                );

                            }

                        }
                    );

                }

            }
        );

        /* =============================================
        COLLAPSIBLE LESSON PARTS
        ============================================= */

        const partHeadings =
            Array.from(
                content.children
            ).filter(
                function (element) {

                    const headingText =
                        element.textContent.trim();

                    return (
                        element.tagName === "H1"
                        &&
                        (
                            headingText === "Knowledge"
                            ||
                            headingText === "Risk Management"
                            ||
                            headingText === "Skills"
                        )
                    );
                }
            );


        partHeadings.forEach(
            function (heading) {

                const part =
                    document.createElement(
                        "section"
                    );

                part.className =
                    "lesson-part";


                const body =
                    document.createElement(
                        "div"
                    );

                body.className =
                    "lesson-part-body";


                content.insertBefore(
                    part,
                    heading
                );

                part.appendChild(
                    heading
                );

                part.appendChild(
                    body
                );


                /*
                * Move everything after this Part heading
                * into the Part until the next Part heading.
                */
                while (
                    part.nextSibling
                ) {

                    const next =
                        part.nextSibling;

                    if (
                        next.nodeType
                            === Node.ELEMENT_NODE
                        &&
                        next.tagName === "H1"
                    ) {

                        const nextHeadingText =
                            next.textContent.trim();

                        if (
                            nextHeadingText === "Knowledge"
                            ||
                            nextHeadingText === "Risk Management"
                            ||
                            nextHeadingText === "Skills"
                        ) {
                            break;
                        }
                    }

                    body.appendChild(
                        next
                    );
                }


                const headingHtml =
                    heading.innerHTML;

                heading.innerHTML = "";

                heading.classList.add(
                    "lesson-part-heading"
                );


                const button =
                    document.createElement(
                        "button"
                    );

                button.type =
                    "button";

                button.className =
                    "lesson-part-toggle";

                button.setAttribute(
                    "aria-expanded",
                    "true"
                );


                const title =
                    document.createElement(
                        "span"
                    );

                title.className =
                    "lesson-part-title";

                title.innerHTML =
                    headingHtml;


                const chevron =
                    document.createElement(
                        "span"
                    );

                chevron.className =
                    "lesson-part-chevron";

                chevron.setAttribute(
                    "aria-hidden",
                    "true"
                );

                chevron.textContent =
                    "›";


                button.appendChild(
                    title
                );

                button.appendChild(
                    chevron
                );

                heading.appendChild(
                    button
                );


                button.addEventListener(
                    "click",
                    function () {

                        const collapsed =
                            part.classList.toggle(
                                "collapsed"
                            );

                        body.hidden =
                            collapsed;

                        button.setAttribute(
                            "aria-expanded",
                            collapsed
                                ? "false"
                                : "true"
                        );
                    }
                );
            }
        );

        /* =============================================
           SHOW / HIDE ANSWERS
        ============================================= */

        const answers =
            document.querySelectorAll(
                ".lesson-answer"
            );


        answers.forEach(
            function (answer) {

                const summary =
                    answer.querySelector(
                        "summary"
                    );

                if (!summary) {
                    return;
                }


                function updateLabel() {

                    summary.textContent =
                        answer.open
                            ? "Hide Answer"
                            : "Show Answer";

                }


                updateLabel();


                answer.addEventListener(
                    "toggle",
                    updateLabel
                );

            }
        );


        /* =============================================
           CONSTRAINED YOUTUBE EXCERPTS
        ============================================= */

        const pdfEmbeds =
            Array.from(
                document.querySelectorAll(
                    ".pdf-embed-lazy"
                )
            );

        pdfEmbeds.forEach(
            function (embed) {

                const toggle =
                    embed.querySelector(
                        ".pdf-source-toggle"
                    );

                const viewer =
                    embed.querySelector(
                        ".pdf-viewer"
                    );

                const action =
                    embed.querySelector(
                        ".pdf-source-action"
                    );

                if (!toggle || !viewer) {
                    return;
                }

                toggle.addEventListener(
                    "click",
                    function () {

                        let iframe =
                            viewer.querySelector(
                                "iframe"
                            );

                        if (!iframe) {

                            const source =
                                embed.dataset.pdfSrc;

                            if (!source) {
                                return;
                            }

                            iframe =
                                document.createElement(
                                    "iframe"
                                );

                            iframe.src = source;
                            iframe.loading = "lazy";
                            iframe.title =
                                "PDF document";

                            viewer.appendChild(
                                iframe
                            );

                        }

                        const isOpen =
                            !viewer.hidden;

                        viewer.hidden = isOpen;

                        toggle.setAttribute(
                            "aria-expanded",
                            isOpen
                                ? "false"
                                : "true"
                        );

                        if (action) {
                            action.textContent =
                                isOpen
                                    ? "View Source"
                                    : "Hide Source";
                        }

                    }
                );

            }
        );

        const youtubeSegments =
            Array.from(
                document.querySelectorAll(
                    ".youtube-segment"
                )
            );

        if (youtubeSegments.length === 0) {
            return;
        }


        function loadYouTubeApi() {

            if (
                window.YT
                && window.YT.Player
            ) {
                return Promise.resolve(
                    window.YT
                );
            }


            if (window.__cfiYouTubeApiPromise) {
                return window.__cfiYouTubeApiPromise;
            }


            window.__cfiYouTubeApiPromise =
                new Promise(
                    function (resolve, reject) {

                        const previousReady =
                            window.onYouTubeIframeAPIReady;


                        window.onYouTubeIframeAPIReady =
                            function () {

                                if (
                                    typeof previousReady
                                    === "function"
                                ) {
                                    previousReady();
                                }

                                resolve(
                                    window.YT
                                );

                            };


                        let script =
                            document.querySelector(
                                'script[src="https://www.youtube.com/iframe_api"]'
                            );


                        if (!script) {

                            script =
                                document.createElement(
                                    "script"
                                );

                            script.src =
                                "https://www.youtube.com/iframe_api";

                            script.async = true;

                            script.onerror =
                                function () {
                                    reject(
                                        new Error(
                                            "YouTube IFrame API failed to load."
                                        )
                                    );
                                };

                            document.head.appendChild(
                                script
                            );

                        }


                        /*
                         * Fallback in case another script loaded
                         * the API and consumed the global callback.
                         */

                        const started = Date.now();

                        const waitForApi =
                            window.setInterval(
                                function () {

                                    if (
                                        window.YT
                                        && window.YT.Player
                                    ) {

                                        window.clearInterval(
                                            waitForApi
                                        );

                                        resolve(
                                            window.YT
                                        );

                                        return;
                                    }


                                    if (
                                        Date.now() - started
                                        > 10000
                                    ) {

                                        window.clearInterval(
                                            waitForApi
                                        );

                                        reject(
                                            new Error(
                                                "Timed out loading YouTube IFrame API."
                                            )
                                        );

                                    }

                                },
                                100
                            );

                    }
                );


            return window.__cfiYouTubeApiPromise;

        }


        function formatSegmentTime(seconds) {

            if (
                !Number.isFinite(seconds)
                || seconds < 0
            ) {
                seconds = 0;
            }

            seconds = Math.floor(seconds);

            const hours =
                Math.floor(
                    seconds / 3600
                );

            const minutes =
                Math.floor(
                    (seconds % 3600) / 60
                );

            const secs =
                seconds % 60;


            if (hours > 0) {
                return (
                    hours
                    + ":"
                    + String(minutes).padStart(2, "0")
                    + ":"
                    + String(secs).padStart(2, "0")
                );
            }


            return (
                minutes
                + ":"
                + String(secs).padStart(2, "0")
            );

        }


        function initializeYouTubeSegment(
            segment,
            index,
            YT
        ) {

            const videoId =
                segment.dataset.videoId;

            const startSeconds =
                Number(
                    segment.dataset.start || 0
                );

            const configuredEnd =
                segment.dataset.end
                    ? Number(segment.dataset.end)
                    : null;


            const playerNode =
                segment.querySelector(
                    ".youtube-segment-player"
                );

            const cover =
                segment.querySelector(
                    ".youtube-segment-cover"
                );

            const playButton =
                segment.querySelector(
                    ".youtube-segment-play"
                );

            const progress =
                segment.querySelector(
                    ".youtube-segment-progress"
                );

            const timeLabel =
                segment.querySelector(
                    ".youtube-segment-time"
                );


            if (
                !videoId
                || !playerNode
                || !cover
                || !playButton
                || !progress
                || !timeLabel
            ) {
                return;
            }


            playerNode.id =
                "youtube-segment-player-"
                + index;


            let player = null;
            let segmentEnd = configuredEnd;
            let isDragging = false;
            let ready = false;


            function segmentLength() {

                if (
                    segmentEnd === null
                    || !Number.isFinite(segmentEnd)
                ) {
                    return 0;
                }

                return Math.max(
                    0,
                    segmentEnd - startSeconds
                );

            }


            function relativeTimeFromSlider() {

                const length =
                    segmentLength();

                if (length <= 0) {
                    return 0;
                }

                return (
                    Number(progress.value)
                    / Number(progress.max)
                ) * length;

            }


            function updateTimeLabel(
                relativeSeconds
            ) {

                timeLabel.textContent =
                    formatSegmentTime(
                        relativeSeconds
                    )
                    + " / "
                    + formatSegmentTime(
                        segmentLength()
                    );

            }


            function setPlayButtonState(
                isPlaying
            ) {

                playButton.textContent =
                    isPlaying
                        ? "❚❚"
                        : "▶";

                playButton.setAttribute(
                    "aria-label",
                    isPlaying
                        ? "Pause video excerpt"
                        : "Play video excerpt"
                );

            }


            function setProgressFromAbsoluteTime(
                absoluteTime
            ) {

                const length =
                    segmentLength();

                if (length <= 0) {
                    progress.value = "0";
                    updateTimeLabel(0);
                    return;
                }

                const relative =
                    Math.min(
                        length,
                        Math.max(
                            0,
                            absoluteTime - startSeconds
                        )
                    );

                progress.value = String(
                    Math.round(
                        (relative / length)
                        * Number(progress.max)
                    )
                );

                updateTimeLabel(
                    relative
                );

            }


            function resolveUnboundedEnd() {

                if (
                    segmentEnd !== null
                    || !player
                ) {
                    return;
                }

                const duration =
                    Number(
                        player.getDuration()
                    );

                if (
                    Number.isFinite(duration)
                    && duration > startSeconds
                ) {
                    segmentEnd = duration;
                }

            }


            function clampAbsoluteTime(
                absoluteTime
            ) {

                resolveUnboundedEnd();

                if (segmentEnd === null) {
                    return Math.max(
                        startSeconds,
                        absoluteTime
                    );
                }

                /*
                 * Stay a fraction inside the endpoint when
                 * actively seeking.  The displayed slider can
                 * still show 100% when playback reaches the end.
                 */

                const latestSeek =
                    Math.max(
                        startSeconds,
                        segmentEnd - 0.05
                    );

                return Math.min(
                    latestSeek,
                    Math.max(
                        startSeconds,
                        absoluteTime
                    )
                );

            }


            function seekFromSlider(
                allowSeekAhead
            ) {

                if (!ready || !player) {
                    return;
                }

                const relative =
                    relativeTimeFromSlider();

                const target =
                    clampAbsoluteTime(
                        startSeconds + relative
                    );

                const state =
                    player.getPlayerState();

                const wasPlaying =
                    state === YT.PlayerState.PLAYING;


                player.seekTo(
                    target,
                    allowSeekAhead
                );


                /*
                 * YouTube can begin playback when seekTo() is
                 * called from a cued state. Preserve the user's
                 * prior play/pause intent.
                 */

                if (!wasPlaying) {
                    window.setTimeout(
                        function () {
                            player.pauseVideo();
                        },
                        40
                    );
                }

            }


            function enforceSegmentBounds() {

                if (!ready || !player) {
                    return;
                }

                resolveUnboundedEnd();

                const current =
                    Number(
                        player.getCurrentTime()
                    );

                if (!Number.isFinite(current)) {
                    return;
                }


                const state =
                    player.getPlayerState();


                if (
                    current < startSeconds - 0.25
                ) {

                    player.seekTo(
                        startSeconds,
                        true
                    );

                    if (
                        state !== YT.PlayerState.PLAYING
                    ) {
                        player.pauseVideo();
                    }

                    setProgressFromAbsoluteTime(
                        startSeconds
                    );

                    return;
                }


                if (
                    segmentEnd !== null
                    && current >= segmentEnd - 0.05
                ) {

                    player.pauseVideo();

                    progress.value =
                        progress.max;

                    updateTimeLabel(
                        segmentLength()
                    );

                    setPlayButtonState(
                        false
                    );

                    return;
                }


                if (!isDragging) {
                    setProgressFromAbsoluteTime(
                        current
                    );
                }


                setPlayButtonState(
                    state === YT.PlayerState.PLAYING
                );

            }


            player = new YT.Player(
                playerNode.id,
                {
                    width: "100%",
                    height: "100%",
                    videoId: videoId,

                    playerVars: {
                        controls: 0,
                        disablekb: 1,
                        playsinline: 1,
                        rel: 0,
                        origin: window.location.origin
                    },

                    events: {

                        onReady: function (event) {

                            const cueOptions = {
                                videoId: videoId,
                                startSeconds: startSeconds
                            };

                            if (
                                configuredEnd !== null
                            ) {
                                cueOptions.endSeconds =
                                    configuredEnd;
                            }


                            event.target.cueVideoById(
                                cueOptions
                            );

                            ready = true;


                            window.setTimeout(
                                function () {

                                    resolveUnboundedEnd();

                                    setProgressFromAbsoluteTime(
                                        startSeconds
                                    );

                                    setPlayButtonState(
                                        false
                                    );

                                },
                                100
                            );

                        },

                        onStateChange: function (event) {

                            const isPlaying =
                                event.data
                                === YT.PlayerState.PLAYING;

                            setPlayButtonState(
                                isPlaying
                            );

                            /*
                            * Hide the Flight Guide cover only
                            * while the actual video is playing.
                            */
                            cover.hidden =
                                isPlaying;

                            if (
                                event.data
                                === YT.PlayerState.ENDED
                            ) {

                                progress.value =
                                    progress.max;

                                updateTimeLabel(
                                    segmentLength()
                                );

                                cover.hidden =
                                    false;
                            }

                        }

                    }
                }
            );


            playButton.addEventListener(
                "click",
                function () {

                    if (!ready || !player) {
                        return;
                    }

                    resolveUnboundedEnd();

                    const state =
                        player.getPlayerState();


                    if (
                        state === YT.PlayerState.PLAYING
                    ) {
                        player.pauseVideo();
                        return;
                    }


                    const current =
                        Number(
                            player.getCurrentTime()
                        );


                    if (
                        !Number.isFinite(current)
                        || current < startSeconds - 0.25
                        || (
                            segmentEnd !== null
                            && current >= segmentEnd - 0.25
                        )
                    ) {

                        player.seekTo(
                            startSeconds,
                            true
                        );

                    }


                    player.playVideo();

                }
            );


            progress.addEventListener(
                "pointerdown",
                function () {
                    isDragging = true;
                }
            );


            progress.addEventListener(
                "input",
                function () {

                    isDragging = true;

                    updateTimeLabel(
                        relativeTimeFromSlider()
                    );

                    seekFromSlider(
                        false
                    );

                }
            );


            progress.addEventListener(
                "change",
                function () {

                    seekFromSlider(
                        true
                    );

                    isDragging = false;

                }
            );


            progress.addEventListener(
                "pointerup",
                function () {

                    seekFromSlider(
                        true
                    );

                    isDragging = false;

                }
            );


            progress.addEventListener(
                "pointercancel",
                function () {
                    isDragging = false;
                }
            );


            window.setInterval(
                enforceSegmentBounds,
                200
            );

        }


        function initializeYouTubeSegmentOnce(
            segment,
            index
        ) {

            if (
                segment.dataset.youtubeInitialized
                === "true"
                || segment.dataset.youtubeInitializing
                === "true"
            ) {
                return;
            }

            segment.dataset.youtubeInitializing =
                "true";

            loadYouTubeApi()
                .then(
                    function (YT) {

                        segment.dataset.youtubeInitialized =
                            "true";

                        initializeYouTubeSegment(
                            segment,
                            index,
                            YT
                        );

                    }
                )
                .catch(
                    function (error) {

                        delete segment.dataset.youtubeInitializing;

                        console.error(
                            "YouTube excerpt player error:",
                            error
                        );

                        segment.classList.add(
                            "youtube-segment-error"
                        );

                    }
                );

        }


        if (
            "IntersectionObserver" in window
        ) {

            const youtubeObserver =
                new IntersectionObserver(
                    function (entries) {

                        entries.forEach(
                            function (entry) {

                                if (
                                    !entry.isIntersecting
                                ) {
                                    return;
                                }

                                youtubeObserver.unobserve(
                                    entry.target
                                );

                                initializeYouTubeSegmentOnce(
                                    entry.target,
                                    youtubeSegments.indexOf(
                                        entry.target
                                    )
                                );

                            }
                        );

                    },
                    {
                        rootMargin:
                            "300px 0px",
                    }
                );

            youtubeSegments.forEach(
                function (segment) {
                    youtubeObserver.observe(
                        segment
                    );
                }
            );

        } else {

            youtubeSegments.forEach(
                function (segment, index) {
                    initializeYouTubeSegmentOnce(
                        segment,
                        index
                    );
                }
            );

        }

    }
);