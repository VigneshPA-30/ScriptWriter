// ScriptWriter SPA logic
const PAGES = ["niche", "find-topic", "topic-research", "hook-generation", "full-script"];
const HEADINGS = ["find-topic", "topic-research", "hook-generation", "full-script"];
const API_URL = 'http://127.0.0.1:8000'; // Backend API URL

let state = {
    page: 0, // 0: niche, 1: find-topic, 2: topic-research, 3: hook-generation, 4: full-script
    niche: '',
    auto: false, // manual by default
    topics: [],
    selectedTopic: null,
    research: '',
    hooks: [],
    selectedHook: null,
    script: '',
    sources: [],
    enabled: [true, false, false, false, false],
    loading: false,
};

function render() {
    const app = document.getElementById('app');
    app.innerHTML = '';
    document.body.setAttribute('data-page', state.page);
    // Header with navigation buttons
    const header = document.createElement('div');
    header.className = 'header';
    const headingBtns = document.createElement('div');
    headingBtns.className = 'heading-btns';
    HEADINGS.forEach((h, i) => {
        const btn = document.createElement('button');
        btn.className = 'heading-btn' + (state.page === i+1 ? ' active' : '');
        btn.innerText = headingLabel(h);
        btn.disabled = false; // Never disable navigation buttons
        btn.onclick = () => { state.page = i+1; render(); };
        headingBtns.appendChild(btn);
    });
    header.appendChild(headingBtns);
    app.appendChild(header);

    // Main content
    if(state.page === 0) renderNichePage(app);
    else if(state.page === 1) renderFindTopicPage(app);
    else if(state.page === 2) renderTopicResearchPage(app);
    else if(state.page === 3) renderHookGenerationPage(app);
    else if(state.page === 4) renderFullScriptPage(app);

    // Page navigation
    const nav = document.createElement('div');
    nav.className = 'page-nav';
    const prevBtn = document.createElement('button');
    prevBtn.className = 'page-btn';
    prevBtn.innerText = 'Previous';
    prevBtn.disabled = state.page === 0;
    prevBtn.onclick = () => { if(state.page > 0) { state.page--; render(); } };
    nav.appendChild(prevBtn);
    const nextBtn = document.createElement('button');
    nextBtn.className = 'page-btn';
    nextBtn.innerText = 'Next';
    nextBtn.disabled = state.page === 4 || state.loading ||
        (state.page === 1 && state.selectedTopic === null) ||
        (state.page === 2 && !state.research) ||
        (state.page === 3 && !state.hooks[0]);
    nextBtn.onclick = () => handleNext();
    nav.appendChild(nextBtn);
    app.appendChild(nav);
}

function headingLabel(h) {
    if(h === 'find-topic') return 'Find Topic';
    if(h === 'topic-research') return 'Topic Research';
    if(h === 'hook-generation') return 'Hook Generation';
    if(h === 'full-script') return 'Full Script';
    return h;
}

function renderNichePage(app) {
    // Toggle group
    const toggle = document.createElement('div');
    toggle.className = 'toggle-group';
    const btn = document.createElement('button');
    btn.className = 'toggle-btn' + (state.auto ? ' selected' : '');
    btn.onclick = () => {
        state.auto = !state.auto;
        render();
    };
    toggle.appendChild(btn);
    const label = document.createElement('span');
    label.textContent = 'Complete Automatic';
    toggle.appendChild(label);
    app.appendChild(toggle);
    
    // Niche input
    const input = document.createElement('input');
    input.className = 'niche-input';
    input.placeholder = 'Enter your niche...';
    input.value = state.niche;
    app.appendChild(input);
    
    // Go button
    const goBtn = document.createElement('button');
    goBtn.className = 'go-btn';
    goBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>';
    goBtn.disabled = !state.niche.trim(); // Only disabled if no niche entered
    goBtn.onclick = async () => {
        try {
            state.loading = true;
            state.page = 1;
            render();
            // 1. First get the topics
            const topicsResponse = await fetch(`${API_URL}/research/topics`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({ niche: state.niche })
            });
            const topicsData = await topicsResponse.json();
            state.topics = topicsData.content.split('\n').filter(topic => topic.trim());
            state.loading = false;
            render();

            if (state.auto) {
                // In automatic mode, randomly select a topic
                const randomIndex = Math.floor(Math.random() * state.topics.length);
                const selectedTopic = state.topics[randomIndex];
                state.selectedTopic = randomIndex;

                // 2. Get research for the randomly selected topic
                state.loading = true;
                state.page = 2;
                render();
                const researchResponse = await fetch(`${API_URL}/research/topic`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    mode: 'cors',
                    credentials: 'include',
                    body: JSON.stringify({
                        topic: selectedTopic,
                        topic_selected: randomIndex,
                        is_auto: true
                    })
                });
                const researchData = await researchResponse.json();
                state.research = researchData.research || researchData.content;
                state.sources = researchData.sources || [];
                state.loading = false;
                render();

                // 3. Generate hook
                state.loading = true;
                state.page = 3;
                render();
                const hookResponse = await fetch(`${API_URL}/generate/hook`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    mode: 'cors',
                    credentials: 'include',
                    body: JSON.stringify({
                        research_report: state.research,
                        is_auto: true
                    })
                });
                const hookData = await hookResponse.json();
                state.hooks = [hookData.content];
                state.loading = false;
                render();

                // 4. Generate script
                state.loading = true;
                state.page = 4;
                render();
                const scriptResponse = await fetch(`${API_URL}/generate/script`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    mode: 'cors',
                    credentials: 'include',
                    body: JSON.stringify({
                        hook: state.hooks[0],
                        research_report: state.research
                    })
                });
                const scriptData = await scriptResponse.json();
                state.script = scriptData.content;
                state.loading = false;
                // Enable all pages and navigate to the final script
                state.enabled = [true, true, true, true, true];
                render();
            } else {
                // In manual mode, just enable the topic selection page
                state.enabled[1] = true;
            }
        } catch (error) {
            console.error('Error in workflow:', error);
            alert('An error occurred. Please try again.');
        }
    };
    input.oninput = e => {
        state.niche = e.target.value;
        goBtn.disabled = !state.niche.trim();
    };
    app.appendChild(goBtn);
}

function renderFindTopicPage(app) {
    if (state.loading) {
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerText = 'Loading...';
        app.appendChild(loading);
        return;
    }

    // Topic buttons
    const boxBtns = document.createElement('div');
    boxBtns.className = 'box-btns';
    state.topics.forEach((topic, i) => {
        const btn = document.createElement('button');
        btn.className = 'box-btn' + (state.selectedTopic === i ? ' selected' : '');
        btn.innerText = topic;
        btn.onclick = () => {
            state.selectedTopic = i;
            render();
        };
        boxBtns.appendChild(btn);
    });
    app.appendChild(boxBtns);
}

function renderTopicResearchPage(app) {
    if (state.loading) {
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerText = 'Loading...';
        app.appendChild(loading);
        return;
    }

    // Scrollable text
    const scroll = document.createElement('div');
    scroll.className = 'scrollable-text';
    scroll.innerText = state.research || 'Select a topic to see research.';
    app.appendChild(scroll);

    const sourcesBtn = document.createElement('button');
    sourcesBtn.className = 'sources-btn';
    sourcesBtn.innerText = 'Sources';
    sourcesBtn.onclick = () => alert('Sources: ' + (state.sources.length ? state.sources.join(', ') : 'None yet'));
    app.appendChild(sourcesBtn);
}

function renderHookGenerationPage(app) {
    if (state.loading) {
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerText = 'Loading...';
        app.appendChild(loading);
        return;
    }

    // Display generated hook
    const scroll = document.createElement('div');
    scroll.className = 'scrollable-text';
    scroll.innerText = state.hooks[0] || 'No hook yet.';
    app.appendChild(scroll);
}

function renderFullScriptPage(app) {
    if (state.loading) {
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerText = 'Loading...';
        app.appendChild(loading);
        return;
    }

    // Scrollable text
    const scroll = document.createElement('div');
    scroll.className = 'scrollable-text';
    scroll.innerText = state.script || 'Select a hook to generate the script.';
    app.appendChild(scroll);
}

async function handleNext() {
    try {
        if (state.page === 1 && state.selectedTopic !== null) {
            state.loading = true;
            state.page = 2;
            render();
            const topic = state.topics[state.selectedTopic];
            const response = await fetch(`${API_URL}/research/topic`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({
                    topic: topic,
                    topic_selected: state.selectedTopic,
                    is_auto: false
                })
            });
            const data = await response.json();
            state.research = data.research || data.content;
            state.sources = data.sources || [];
            state.loading = false;
            render();
        } else if (state.page === 2 && state.research) {
            state.loading = true;
            state.page = 3;
            render();
            const response = await fetch(`${API_URL}/generate/hook`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({
                    research_report: state.research,
                    is_auto: state.auto
                })
            });
            const data = await response.json();
            state.hooks = [data.content];
            state.loading = false;
            render();
        } else if (state.page === 3 && state.hooks[0]) {
            state.loading = true;
            state.page = 4;
            render();
            const response = await fetch(`${API_URL}/generate/script`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({
                    hook: state.hooks[0],
                    research_report: state.research
                })
            });
            const data = await response.json();
            state.script = data.content;
            state.loading = false;
            render();
        } else if (state.page < 4) {
            state.page++;
            render();
        }
    } catch (error) {
        console.error('Error in navigation workflow:', error);
        alert('An error occurred. Please try again.');
        state.loading = false;
        render();
    }
}

document.addEventListener('DOMContentLoaded', render);
