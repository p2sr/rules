document.querySelectorAll("nav img, nav a").forEach(e => {
    e.addEventListener("click", () => {
        document.querySelector("nav").classList.toggle("visible");
    })
});
