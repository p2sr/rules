(function(){
    function formatDate(epoch, fmt){
        const d = new Date(Number(epoch) * 1000);
        switch(fmt){
            case 't': return d.toLocaleTimeString(undefined, {hour: 'numeric', minute: '2-digit'});
            case 'T': return d.toLocaleTimeString(undefined, {hour: 'numeric', minute: '2-digit', second: '2-digit'});
            case 'd': return d.toLocaleDateString();
            case 'D': return d.toLocaleDateString(undefined, {year:'numeric', month:'long', day:'numeric'});
            case 'f': return d.toLocaleString(undefined, {year:'numeric', month:'short', day:'numeric', hour:'numeric', minute:'2-digit'});
            case 'F': return d.toLocaleString(undefined, {weekday:'long', year:'numeric', month:'long', day:'numeric', hour:'numeric', minute:'2-digit'});
            case 'R': return relativeTime(new Date(Number(epoch) * 1000));
            default: return d.toString();
        }
    }

    function relativeTime(date){
        const now = Date.now();
        let diff = Math.floor((now - date.getTime()) / 1000);
        if (Math.abs(diff) < 5) return 'just now';
        const intervals = [
            [60, 'second', 1],
            [3600, 'minute', 60],
            [86400, 'hour', 3600],
            [604800, 'day', 86400],
            [2629800, 'week', 604800],
            [31557600, 'month', 2629800],
            [Number.MAX_SAFE_INTEGER, 'year', 31557600]
        ];
        const past = diff > 0;
        diff = Math.abs(diff);
        for (let i = 0; i < intervals.length; i++){
            if (diff < intervals[i][0]){
                const val = Math.floor(diff / intervals[i][2]) || 0;
                const unit = intervals[i][1] + (val === 1 ? '' : 's');
                return past ? `${val} ${unit} ago` : `in ${val} ${unit}`;
            }
        }
        return '';
    }

    function renderElement(el){
        const epoch = el.getAttribute('data-epoch');
        const fmt = el.getAttribute('data-format') || 'f';
        if (!epoch) return;
        el.textContent = formatDate(epoch, fmt);
        el.title = new Date(Number(epoch) * 1000).toLocaleString();
    }

    // Schedule updates per-element for relative timestamps
    function scheduleRelative(el){
        // Render now
        renderElement(el);

        // Compute next update delay based on current distance
        const epochMs = Number(el.getAttribute('data-epoch')) * 1000;
        const now = Date.now();
        let diff = Math.floor((now - epochMs) / 1000);
        const absDiff = Math.abs(diff);

        let unitSeconds;
        if (absDiff < 60) unitSeconds = 1; // seconds
        else if (absDiff < 3600) unitSeconds = 60; // minutes
        else if (absDiff < 86400) unitSeconds = 3600; // hours
        else if (absDiff < 604800) unitSeconds = 86400; // days
        else if (absDiff < 2629800) unitSeconds = 604800; // weeks
        else if (absDiff < 31557600) unitSeconds = 2629800; // months
        else unitSeconds = 31557600; // years

        const remainder = absDiff % unitSeconds;
        let nextSeconds = remainder === 0 ? unitSeconds : (unitSeconds - remainder);
        if (nextSeconds < 1) nextSeconds = 1;

        // Clear previous timer if any
        if (el._timeoutId) clearTimeout(el._timeoutId);

        el._timeoutId = setTimeout(function(){
            // On timeout, re-schedule (this will re-render and compute next delay)
            scheduleRelative(el);
        }, nextSeconds * 1000);
    }

    function init(){
        // Render non-relative timestamps once
        document.querySelectorAll('time.discord-timestamp').forEach(function(el){
            const fmt = el.getAttribute('data-format') || 'f';
            if (fmt === 'R'){
                scheduleRelative(el);
            } else {
                renderElement(el);
            }
        });
    }

    document.addEventListener('DOMContentLoaded', init);
})();
