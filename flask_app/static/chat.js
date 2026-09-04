document.addEventListener(
    "DOMContentLoaded",
    () => {

    const body = document.body;

    const currentPath =
        body.dataset.currentPath || "/";

    const hasLesson =
        body.dataset.hasLesson === "true";


    // =====================================================
    // STORAGE
    // =====================================================

    function libraryStorageKey() {
        return "aviation_chat_library";
    }


    function lessonStorageKey() {
        return (
            "aviation_chat_lesson::"
            + currentPath
        );
    }


    function blankState() {

        return {
            previousResponseId: null,
            lastSiteUrl: null,
            messages: []
        };

    }


    function loadState(key) {

        try {

            const stored =
                sessionStorage.getItem(key);

            if (!stored) {
                return blankState();
            }

            return JSON.parse(stored);

        }

        catch {

            return blankState();

        }

    }


    function saveState(
        key,
        state
    ) {

        sessionStorage.setItem(
            key,
            JSON.stringify(state)
        );

    }


    // =====================================================
    // DRAWERS
    // =====================================================

    const overlay =
        document.getElementById(
            "assistant-overlay"
        );


    const libraryDrawer =
        document.getElementById(
            "library-assistant-drawer"
        );


    const lessonDrawer =
        document.getElementById(
            "lesson-assistant-drawer"
        );


    function closeDrawers() {

        if (libraryDrawer) {
            libraryDrawer.classList.remove(
                "open"
            );
        }

        if (lessonDrawer) {
            lessonDrawer.classList.remove(
                "open"
            );
        }

        overlay.classList.remove(
            "open"
        );

    }


    function openDrawer(drawer) {

        closeDrawers();

        drawer.classList.add(
            "open"
        );

        overlay.classList.add(
            "open"
        );

    }


    document.getElementById(
        "open-library-assistant"
    ).addEventListener(
        "click",
        () => {

            openDrawer(
                libraryDrawer
            );

            document.getElementById(
                "library-input"
            ).focus();

        }
    );


    if (hasLesson) {

        document.getElementById(
            "open-lesson-assistant"
        ).addEventListener(
            "click",
            () => {

                openDrawer(
                    lessonDrawer
                );

                document.getElementById(
                    "lesson-input"
                ).focus();

            }
        );

    }


    document.querySelectorAll(
        "[data-close-assistant]"
    ).forEach(
        button => {

            button.addEventListener(
                "click",
                closeDrawers
            );

        }
    );


    overlay.addEventListener(
        "click",
        closeDrawers
    );


    document.addEventListener(
        "keydown",
        event => {

            if (event.key === "Escape") {
                closeDrawers();
            }

        }
    );


    // =====================================================
    // DISPLAY HELPERS
    // =====================================================

    function scrollToBottom(container) {

        container.scrollTop =
            container.scrollHeight;

    }


    function createMessageBubble(
        role,
        text
    ) {

        const wrapper =
            document.createElement("div");

        wrapper.className =
            "chat-message "
            + (
                role === "user"
                ? "user-message"
                : "assistant-message"
            );


        const bubble =
            document.createElement("div");

        bubble.className =
            "chat-bubble";


        const paragraphs =
            text.split(/\n{2,}/);


        paragraphs.forEach(
            paragraph => {

                if (!paragraph.trim()) {
                    return;
                }

                const p =
                    document.createElement("p");

                p.textContent =
                    paragraph.trim();

                bubble.appendChild(p);

            }
        );


        wrapper.appendChild(
            bubble
        );

        return {
            wrapper,
            bubble
        };

    }


    function addSources(
        bubble,
        sources
    ) {

        if (
            !Array.isArray(sources)
            || sources.length === 0
        ) {
            return;
        }


        const box =
            document.createElement("div");

        box.className =
            "chat-sources";


        const heading =
            document.createElement("div");

        heading.className =
            "chat-sources-title";

        heading.textContent =
            "Sources";

        box.appendChild(
            heading
        );


        sources.forEach(
            source => {

                const link =
                    document.createElement("a");

                link.className =
                    "chat-source-link";

                link.href =
                    source.url;

                link.target =
                    "_blank";

                link.rel =
                    "noopener noreferrer";


                const title =
                    document.createElement("span");

                title.className =
                    "chat-source-title";

                title.textContent =
                    source.title;


                const authority =
                    document.createElement("span");

                authority.className =
                    "chat-source-authority";

                authority.textContent =
                    source.authority || "";


                link.appendChild(title);
                link.appendChild(authority);

                box.appendChild(link);

            }
        );


        bubble.appendChild(
            box
        );

    }

    function addReferences(
        bubble,
        references
    ) {

        if (
            !Array.isArray(references)
            || references.length === 0
        ) {
            return;
        }


        const box =
            document.createElement("div");

        box.className =
            "chat-references";


        const heading =
            document.createElement("div");

        heading.className =
            "chat-references-title";

        heading.textContent =
            "References";

        box.appendChild(
            heading
        );


        references.forEach(
            (reference, index) => {

                const row =
                    document.createElement("div");

                row.className =
                    "chat-reference";


                const number =
                    document.createElement("span");

                number.className =
                    "chat-reference-number";

                number.textContent =
                    (index + 1) + ".";


                const content =
                    document.createElement("div");

                content.className =
                    "chat-reference-content";


                let titleElement;


                if (reference.url) {

                    titleElement =
                        document.createElement("a");

                    titleElement.href =
                        reference.url;

                    titleElement.className =
                        "chat-reference-title";


                    // Site lessons stay in this tab.
                    // FAA/reference documents open separately.

                    if (
                        reference.type
                        === "site"
                    ) {

                        titleElement.target =
                            "_self";

                    }

                    else {

                        titleElement.target =
                            "_blank";

                        titleElement.rel =
                            "noopener noreferrer";

                    }

                }

                else {

                    titleElement =
                        document.createElement("span");

                    titleElement.className =
                        "chat-reference-title";

                }


                titleElement.textContent =
                    reference.title;


                const authority =
                    document.createElement("div");

                authority.className =
                    "chat-reference-authority";

                authority.textContent =
                    reference.authority || "";


                content.appendChild(
                    titleElement
                );

                content.appendChild(
                    authority
                );


                row.appendChild(
                    number
                );

                row.appendChild(
                    content
                );


                box.appendChild(
                    row
                );

            }
        );


        bubble.appendChild(
            box
        );

    }


    function addOpenLessonButton(
        bubble,
        url
    ) {

        if (!url) {
            return;
        }


        const button =
            document.createElement("a");

        button.href = url;

        button.className =
            "chat-open-lesson";

        button.textContent =
            "Open Lesson";

        bubble.appendChild(
            button
        );

    }


    // =====================================================
    // CHAT INSTANCE
    // =====================================================

    function createChat({
        scope,
        storageKey,
        messagesElement,
        formElement,
        inputElement
    }) {

        let state =
            loadState(storageKey);


        function renderStoredMessages() {

            messagesElement.innerHTML = "";


            if (
                state.messages.length === 0
            ) {

                const welcome =
                    document.createElement("div");

                welcome.className =
                    "assistant-welcome";


                if (scope === "library") {

                    welcome.innerHTML =
                        "<strong>What can I help you find?</strong>"
                        + "<p>Ask anything. Answers are grounded in approved aviation sources.</p>";

                }

                else {

                    welcome.innerHTML =
                        "<strong>Ask about this lesson.</strong>"
                        + "<p>This chat uses the exact lesson you are viewing "
                        + "and approved aviation sources.</p>";

                }


                messagesElement.appendChild(
                    welcome
                );

                return;

            }


            state.messages.forEach(
                message => {

                    const result =
                        createMessageBubble(
                            message.role,
                            message.text
                        );


                    if (
                        message.role === "assistant"
                    ) {

                        addReferences(
                            result.bubble,
                            message.references || []
                        );


                        addOpenLessonButton(
                            result.bubble,
                            message.navigateTo
                        );

                    }


                    messagesElement.appendChild(
                        result.wrapper
                    );

                }
            );


            scrollToBottom(
                messagesElement
            );

        }


        renderStoredMessages();


        async function sendMessage(
            message
        ) {

            state.messages.push({
                role: "user",
                text: message
            });

            saveState(
                storageKey,
                state
            );

            renderStoredMessages();


            const loading =
                createMessageBubble(
                    "assistant",
                    "Searching aviation knowledge..."
                );

            loading.wrapper.id =
                "temporary-loading";

            messagesElement.appendChild(
                loading.wrapper
            );

            scrollToBottom(
                messagesElement
            );


            inputElement.disabled = true;


            try {

                const response =
                    await fetch(
                        "/api/chat",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                message: message,
                                scope: scope,
                                current_path:
                                    currentPath,
                                previous_response_id:
                                    state.previousResponseId,
                                last_site_url:
                                    state.lastSiteUrl
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error
                        || "Chat request failed."
                    );

                }


                state.previousResponseId =
                    data.response_id || null;


                state.lastSiteUrl =
                    data.last_site_url || null;


                state.messages.push({
                    role: "assistant",
                    text: data.answer,
                    references:
                        data.references || [],
                    sources:
                        data.sources || [],
                    navigateTo:
                        data.navigate_to || null
                });


                saveState(
                    storageKey,
                    state
                );


                renderStoredMessages();


                // -----------------------------------------
                // EXPLICIT NAVIGATION
                // -----------------------------------------

                if (data.navigate_to) {

                    setTimeout(
                        () => {

                            window.location.href =
                                data.navigate_to;

                        },
                        400
                    );

                }

            }

            catch (error) {

                console.error(error);


                state.messages.push({
                    role: "assistant",
                    text:
                        "Unable to complete the aviation assistant request.",
                    sources: []
                });


                saveState(
                    storageKey,
                    state
                );


                renderStoredMessages();

            }

            finally {

                inputElement.disabled = false;

                inputElement.focus();

            }

        }


        formElement.addEventListener(
            "submit",
            async event => {

                event.preventDefault();


                const message =
                    inputElement.value.trim();


                if (!message) {
                    return;
                }


                inputElement.value = "";


                await sendMessage(
                    message
                );

            }
        );


        inputElement.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter"
                    && !event.shiftKey
                ) {

                    event.preventDefault();

                    formElement.requestSubmit();

                }

            }
        );

    }


    // =====================================================
    // GENERAL CHAT
    // =====================================================

    createChat({

        scope: "library",

        storageKey:
            libraryStorageKey(),

        messagesElement:
            document.getElementById(
                "library-messages"
            ),

        formElement:
            document.getElementById(
                "library-form"
            ),

        inputElement:
            document.getElementById(
                "library-input"
            )

    });


    // =====================================================
    // LESSON CHAT
    // =====================================================

    if (hasLesson) {

        createChat({

            scope: "lesson",

            storageKey:
                lessonStorageKey(),

            messagesElement:
                document.getElementById(
                    "lesson-messages"
                ),

            formElement:
                document.getElementById(
                    "lesson-form"
                ),

            inputElement:
                document.getElementById(
                    "lesson-input"
                )

        });

    }

});