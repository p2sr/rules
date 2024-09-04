document.querySelectorAll("nav img, nav a").forEach(e => {
    e.addEventListener("click", () => {
        document.querySelector("nav").classList.toggle("visible");
        document.querySelector("nav").scrollTo({ top: 0, behavior: "smooth" }); // Reset scroll position
    })
});

window.addEventListener('load', () => {
    document.querySelector("nav").scrollTo({ top: 0 });
});
