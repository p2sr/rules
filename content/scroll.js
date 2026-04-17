{
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
                if (!child.href.includes("#")) continue;
                const id = child.href.substring(child.href.lastIndexOf("#") + 1)
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
        nav.style.background = `linear-gradient(180deg, var(--nav-shadow) ${start}%, #0000 ${end}%)`;
    };

    const addAnchors = () => {
        const headers = main.querySelectorAll("h1, h2, h3, h4, h5, h6");
        for (const header of headers) {
            if (!header.id) continue;
            const anchor = document.createElement("a");
            anchor.href = `#${header.id}`;
            anchor.className = "anchor fa-solid fa-link";
            anchor.onclick = (e) => {
                e.preventDefault();
                navigator.clipboard.writeText(window.location.href.split("#")[0] + `#${header.id}`);
                anchor.style.color = "#4cd";
                setTimeout(() => {
                    anchor.style.removeProperty("color");
                }, 1000);

            }
            // append before
            header.insertBefore(anchor, header.firstChild);
        }
    }

    addAnchors();
    updateScroll();
    main.addEventListener("scroll", updateScroll);
    nav.addEventListener("scroll", updateScroll);
    window.addEventListener("resize", updateScroll);
}
