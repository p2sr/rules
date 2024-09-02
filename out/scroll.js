const nav = document.getElementsByTagName("nav")[0];
const main = document.getElementsByTagName("main")[0]

const calcNavAmounts = (root, root_top, root_bottom, root_min, root_max) => {
    let nav_amounts = [];
    for (const child of root.children) {
        const rect = child.getBoundingClientRect();
        const nest_min = (rect.top - root_top) / (root_bottom - root_top);
        const nest_max = (rect.bottom - root_top) / (root_bottom - root_top);
        const min = root_min + (root_max - root_min) * nest_min;
        const max = root_min + (root_max - root_min) * nest_max;
        if (child.tagName === "A") {
            id = child.href.substring(child.href.lastIndexOf("#") + 1)
            nav_amounts.push({ id: id, min: min, max: max });
        } else {
            nav_amounts = nav_amounts.concat(calcNavAmounts(child, rect.top, rect.bottom, min, max));
        }
    }
    return nav_amounts;
};

const calcAllNavAmounts = () => {
    const rect = nav.getBoundingClientRect();
    return calcNavAmounts(nav, rect.top, rect.bottom, 0.0, 1.0);
};


const updateScroll = () => {
    // Don't change background color on mobile
    if (window.innerWidth < 800) {
        return nav.style.removeProperty("background");
    }

    let min = 0.0;
    let max = 0.0;
    for (const section of calcAllNavAmounts()) {
        const header = document.getElementById(section.id);
        if (main.scrollTop + 1 >= header.offsetTop) {
            min = section.min;
            max = section.max;
        }
    }
    const start = min * 100;
    const end = max * 100;
    nav.style.background = `linear-gradient(180deg, #ffffff10 ${start}%, #0000 ${end}%)`;
};

updateScroll();
main.addEventListener("scroll", updateScroll);
window.addEventListener("resize", updateScroll);
