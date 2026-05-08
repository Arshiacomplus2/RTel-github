const BASE_URL = CONFIG.GITHUB_RAW_BASE_URL;
const CACHE_KEY = "rtel_latest_msgs";

const container = document.getElementById('messages-container');
const loader = document.getElementById('loader');
const refreshBtn = document.getElementById('refresh-btn');

let archiveFiles =[];
let loading = false;


async function init() {
    loadFromCache();
    await fetchLatest();
}


function loadFromCache() {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
        try {
            const msgs = JSON.parse(cached);
            renderMessages(msgs, true);
        } catch (e) {
            console.error("Cache parsing error", e);
        }
    }
}


async function fetchLatest() {
    if (loading) return;
    setLoading(true);

    try {

        const indexRes = await fetch(`${BASE_URL}/data/index.json?t=${Date.now()}`);
        if (indexRes.ok) {
            const indexData = await indexRes.json();

            archiveFiles = indexData.archives ? indexData.archives.reverse() :[];
        }


        const res = await fetch(`${BASE_URL}/data/latest.json?t=${Date.now()}`);
        if (res.ok) {
            const msgs = await res.json();
            localStorage.setItem(CACHE_KEY, JSON.stringify(msgs));
            renderMessages(msgs, true);
        }
    } catch (err) {
        console.error("Failed to fetch latest messages:", err);
    } finally {
        setLoading(false);
    }
}


async function loadMore() {
    if (loading || archiveFiles.length === 0) return;
    setLoading(true);

    try {
        const nextArchive = archiveFiles.shift();
        const res = await fetch(`${BASE_URL}/data/archive/${nextArchive}?t=${Date.now()}`);
        if (res.ok) {
            const msgs = await res.json();
            renderMessages(msgs, false);
        }
    } catch (err) {
        console.error("Failed to fetch archive:", err);
    } finally {
        setLoading(false);
    }
}


function renderMessages(msgs, clear = false) {
    if (clear) container.innerHTML = '';

    msgs.forEach(msg => {
        const dateObj = new Date(msg.date);
        const timeStr = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const dateStr = dateObj.toLocaleDateString();

        const el = document.createElement('div');
        el.className = 'msg-bubble';
        el.innerHTML = `
            <div class="flex justify-between items-center mb-2">
                <span class="font-bold text-blue-600 text-sm">${msg.channel}</span>
                <span class="text-xs text-gray-400">${dateStr} - ${timeStr}</span>
            </div>
            <p class="text-gray-800 text-sm md:text-base leading-relaxed">${formatText(msg.text)}</p>
        `;
        container.appendChild(el);
    });
}


function formatText(text) {
    if (!text) return "";
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
    });
}


function setLoading(status) {
    loading = status;
    loader.classList.toggle('hidden', !status);
}


refreshBtn.addEventListener('click', () => {
    container.innerHTML = '';
    fetchLatest();
});


window.addEventListener('scroll', () => {

    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
        loadMore();
    }
});


init();