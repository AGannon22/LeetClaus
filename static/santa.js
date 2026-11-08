(() => {
    const santa = document.getElementById("flying-santa");
    if (!santa) return;
    const area = santa.parentElement;   // #content
    const img = santa.querySelector("img");
    let x = -santa.offsetWidth;          // start just off the left edge
    let y = area.clientHeight * 0.3;
    function place(nx, ny, seconds) {
        santa.style.transition = `transform ${seconds}s ease-in-out`;
        santa.style.transform = `translate(${nx}px, ${ny}px)`;
    }

    function fly() {
        const maxX = Math.max(area.clientWidth - santa.offsetWidth, 0);
        const maxY = Math.max(area.clientHeight - santa.offsetHeight, 0);
        const nx = Math.random() * maxX;
        const ny = Math.random() * maxY;
        // the rocket points left in the image, so flip it when heading right
        img.classList.toggle("facing-right", nx > x);
        // longer trips take longer, so his speed stays roughly the same
        const seconds = Math.min(Math.max(Math.hypot(nx - x, ny - y) / 140, 1), 6);
        place(nx, ny, seconds);
        x = nx;
        y = ny;
        // hover for a moment at each spot before the next trip
        setTimeout(fly, seconds * 1000 + 600 + Math.random() * 1200);
    }

    place(x, y, 0);
    requestAnimationFrame(() => requestAnimationFrame(fly));   // let the start position apply first
})();
