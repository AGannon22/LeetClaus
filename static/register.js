(() => {
    const button = document.getElementById("registerButton");
    const form = button?.form;
    if (!form) return;
    const registerAudio = new Audio('/static/elevenlabsregisteringsound.mp3');

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        registerAudio.play()
            .then(() => registerAudio.addEventListener("ended", () => form.submit(), { once: true }))
            .catch(() => form.submit());   // if playback fails, still submit
    });
})();
