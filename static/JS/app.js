(() => {
    const PLAY_MS = 340;
    const LEAVE_MS = 190;
    const SCROLL_KEY = "29:scrollY";

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let submitting = false;

    const remember = (fn) => {
        try {
            fn();
        } catch (_) {
            /* storage can be unavailable (private mode); the game still works */
        }
    };

    document.addEventListener("submit", (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;

        if (submitting) {
            event.preventDefault();
            return;
        }

        remember(() => sessionStorage.setItem(SCROLL_KEY, String(window.scrollY)));

        if (reducedMotion) return;

        event.preventDefault();
        submitting = true;

        const isCardPlay = form.classList.contains("card-form");
        if (isCardPlay) {
            form.classList.add("is-played");
            document.body.classList.add("is-playing");
        } else {
            document.body.classList.add("is-leaving");
        }

        window.setTimeout(() => form.submit(), isCardPlay ? PLAY_MS : LEAVE_MS);
    });

    // Replays the plays made since the player's last move, one frame at a time, so each card can be
    // remembered. The server renders every frame; the last one is the live table.
    const startReplay = () => {
        const stack = document.querySelector("[data-replay]");
        if (!stack) return;

        const frames = Array.from(stack.querySelectorAll(".felt-frame"));
        const show = (index) => frames.forEach((frame, i) => frame.classList.toggle("is-active", i === index));
        let index = 0;
        let timer = null;
        let finished = false;

        const finish = () => {
            if (finished) return;
            finished = true;
            window.clearTimeout(timer);
            const live = frames.findIndex((frame) => frame.hasAttribute("data-final"));
            if (live >= 0) show(live);
            document.body.classList.remove("is-replaying");
        };

        const next = () => {
            index += 1;
            const frame = frames[index];
            if (!frame || frame.hasAttribute("data-final")) {
                finish();
                return;
            }
            show(index);
            timer = window.setTimeout(next, Number(frame.dataset.ms) || 2000);
        };

        show(0);
        timer = window.setTimeout(next, Number(frames[0].dataset.ms) || 2000);
        document.querySelector("[data-replay-skip]")?.addEventListener("click", finish);
    };

    startReplay();

    // Coming back via the back button restores the page from cache mid-transition.
    window.addEventListener("pageshow", () => {
        submitting = false;
        document.body.classList.remove("is-leaving", "is-playing");
        document.querySelectorAll(".is-played").forEach((el) => el.classList.remove("is-played"));
    });

    // Each move reloads the page; keep the player where they were instead of jumping to the top.
    remember(() => {
        const saved = sessionStorage.getItem(SCROLL_KEY);
        if (saved !== null) {
            sessionStorage.removeItem(SCROLL_KEY);
            window.scrollTo(0, Number(saved) || 0);
        }
    });
})();
