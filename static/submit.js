(() => {
    const buttons = document.querySelectorAll('button[type="submit"]');
    const leetmasAudio = new Audio('/static/elevenlabsLeetmas.mp3')
    buttons.forEach((button) => {
        const form = button.form;
        if (!form) return;

        form.addEventListener("submit", (event) => {
            event.preventDefault();
            leetmasAudio.play()
                .then(() => leetmasAudio.addEventListener("ended", () => form.submit(), { once: true }))
                .catch(() => form.submit());   // if playback fails, still submit
        });
    });
})();
