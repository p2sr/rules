document.querySelectorAll("nav img, nav a").forEach(e => {
    e.addEventListener("click", () => {
        const navElement = document.querySelector("nav");
        navElement.classList.toggle("visible");
        setTimeout(() => {
            navElement.scrollTo({ top: 0, behavior: "smooth" }); // Reset scroll position 
        }, 0);
    })
});

window.addEventListener('load', () => {
    document.querySelector("nav").scrollTo({ top: 0 });
    fixViewportUnits();
});

window.addEventListener('resize', () => {
    fixViewportUnits();
});

// So basically, turns out some mobile browsers calculate viewport units as a % of the entire screen instead of the viewport itself.
// We're ""fixing"" this by statically replacing styles using "vh" with px values that are calculated on page load for all small screens.
// This is a pretty cursed solution, but at least it works
var viewportStylesheet = document.createElement("style");
document.body.appendChild(viewportStylesheet);
function fixViewportUnits() {
    if (window.innerWidth < 800) {
        const height = `${window.innerHeight}px`;
    
        // Add a new stylesheet to fix the height
        viewportStylesheet.innerHTML = `
            body {
                grid-template-rows: ${height};
            }
            
            nav.visible {
                height: ${height};
            }
        `;
    } else {
        viewportStylesheet.innerHTML = '';
    }
}
