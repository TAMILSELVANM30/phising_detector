const API_BASE = '/api';

// --- Text & URL Scanning ---

async function handleScanText(e) {
    e.preventDefault();
    const text = document.getElementById('scanText').value.trim();
    if (!text) return alert("Please enter some text to scan.");

    showLoader('textLoader');

    try {
        const response = await fetch(`${API_BASE}/scan-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ text })
        });
        const data = await response.json();

        // Save to session storage for result page
        sessionStorage.setItem('scanResult', JSON.stringify(data));
        window.location.href = 'result.html';
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the analysis engine.");
        hideLoader('textLoader');
    }
}

async function handleScanUrl(e) {
    e.preventDefault();
    const url = document.getElementById('scanUrl').value.trim();
    if (!url) return alert("Please enter a URL to scan.");

    showLoader('urlLoader');

    try {
        const response = await fetch(`${API_BASE}/scan-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ url })
        });
        const data = await response.json();

        sessionStorage.setItem('scanResult', JSON.stringify(data));
        window.location.href = 'result.html';
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the analysis engine.");
        hideLoader('urlLoader');
    }
}

// --- Image Scanning (OCR) ---

function handleFileSelect(input) {
    const file = input.files[0];
    if (file) {
        // Show preview
        const reader = new FileReader();
        reader.onload = function (e) {
            const imgPreview = document.getElementById('imgPreview');
            imgPreview.src = e.target.result;
            imgPreview.style.display = 'block';
            document.getElementById('uploadPlaceholder').style.display = 'none';
            document.getElementById('scanBtn').disabled = false;
        }
        reader.readAsDataURL(file);
    }
}

// Drag and drop events for the upload area
const dropArea = document.getElementById('dropArea');
if (dropArea) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('dragover'), false);
    });

    dropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        document.getElementById('fileInput').files = files;
        handleFileSelect(document.getElementById('fileInput'));
    }, false);
}

async function handleScanImage(e) {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) return alert("Please select an image.");

    showLoader('imageLoader');

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    try {
        const response = await fetch(`${API_BASE}/scan-image`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData // No Content-Type header needed; browser boundary will be set
        });
        const data = await response.json();

        sessionStorage.setItem('scanResult', JSON.stringify(data));
        window.location.href = 'result.html';
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to analyze the image.");
        hideLoader('imageLoader');
    }
}

// --- Result Loading logic ---
function loadResults() {
    const resultStr = sessionStorage.getItem('scanResult');
    if (!resultStr) {
        window.location.href = 'dashboard.html';
        return;
    }

    const data = JSON.parse(resultStr);

    // 1. Setup Risk Level Banner
    const riskLevelEl = document.getElementById('riskLevel');
    const riskSubtitleEl = document.getElementById('riskSubtitle');
    const riskIconEl = document.getElementById('riskIcon');

    riskLevelEl.innerText = data.risk_level;

    // Reset classes
    riskIconEl.className = 'pulse-icon';
    riskLevelEl.className = '';

    let colorVar, iconName, subtitle;

    if (data.risk_level === "High Risk") {
        colorVar = 'var(--danger)';
        iconName = 'warning';
        subtitle = "Critical warning! This content matches known scam profiles.";
        riskIconEl.classList.add('bg-high');
        riskLevelEl.classList.add('risk-high');
    } else if (data.risk_level === "Medium Risk") {
        colorVar = 'var(--warning)';
        iconName = 'alert-circle';
        subtitle = "Proceed with caution. Some suspicious elements detected.";
        riskIconEl.classList.add('bg-medium');
        riskLevelEl.classList.add('risk-medium');
    } else {
        colorVar = 'var(--success)';
        iconName = 'shield-checkmark';
        subtitle = "This content appears safe according to our checks.";
        riskIconEl.classList.add('bg-low');
        riskLevelEl.classList.add('risk-low');
    }

    // Insert actual icon HTML
    riskIconEl.innerHTML = `<ion-icon name="${iconName}" style="font-size: 4rem; color: #fff;"></ion-icon>`;
    riskSubtitleEl.innerText = subtitle;

    // 2. Animate Trust Circle
    animateValue(document.getElementById('trustValue'), 0, data.trust_score, 1500);
    const trustCircle = document.getElementById('trustCircle');
    setTimeout(() => {
        trustCircle.style.background = `conic-gradient(${colorVar} ${data.trust_score}%, rgba(255,255,255,0.1) 0%)`;
    }, 100);
    document.getElementById('trustValue').style.color = colorVar;

    // 3. AI Confidence Fill
    const confFill = document.getElementById('aiConfidenceFill');
    const confText = document.getElementById('aiConfidenceText');
    setTimeout(() => {
        confFill.style.width = data.confidence + '%';
        confText.innerText = data.confidence + '%';
    }, 500);

    // 4. Populate Extracted Text if available
    if (data.extracted_text) {
        document.getElementById('extractedSection').style.display = 'block';
        document.getElementById('extractedText').innerText = data.extracted_text;
    }

    // 5. Reasons List
    const reasonsList = document.getElementById('reasonsList');
    if (data.reasons && data.reasons.length > 0) {
        data.reasons.forEach(r => {
            const li = document.createElement('li');
            li.style.color = colorVar;
            li.style.marginBottom = '0.5rem';
            li.innerHTML = `<span style="color:var(--text-main);">${r}</span>`;
            reasonsList.appendChild(li);
        });
    } else {
        reasonsList.innerHTML = `<li style="color:var(--text-muted);">No suspicious patterns found.</li>`;
    }

    // 6. Advice List
    const adviceList = document.getElementById('adviceList');
    if (data.safety_suggestions && data.safety_suggestions.length > 0) {
        data.safety_suggestions.forEach(sa => {
            const li = document.createElement('li');
            li.style.color = 'var(--secondary)';
            li.style.marginBottom = '0.5rem';
            li.innerHTML = `<span style="color:var(--text-main);">${sa}</span>`;
            adviceList.appendChild(li);
        });
    } else {
        adviceList.innerHTML = `<li style="color:var(--text-muted);">Stay vigilant and only trust known sources.</li>`;
    }

    // 7. Educational Explanation (V2)
    const expEl = document.getElementById('detailedExplanation');
    if (expEl && data.detailed_explanation) {
        expEl.innerText = data.detailed_explanation;
    } else if (expEl && data.risk_level === 'Low Risk') {
        expEl.innerText = "This content passed our heuristic and structural checks. No obvious scam patterns were detected.";
    }

    // 8. Dynamic URL Anatomy
    if (data.url_components) {
        const anatomySec = document.getElementById('urlAnatomySection');
        const anatomyContainer = document.getElementById('urlAnatomyContainer');
        if (anatomySec && anatomyContainer) {
            anatomySec.style.display = 'block';

            // Build visual representation
            const { protocol, domain_name, tld, path } = data.url_components;

            let htmlStr = `<div style="font-family: monospace; font-size: 0.95rem; text-align: center; margin-bottom: 1.5rem; word-break: break-all; padding: 0.5rem; background: rgba(0,0,0,0.5); border-radius: 4px;">`;

            if (protocol) htmlStr += `<span style="color: var(--primary-light);">${protocol}</span>`;
            if (domain_name) htmlStr += `<span style="color: var(--secondary);">${domain_name}</span>`;
            if (tld) htmlStr += `<span style="color: var(--accent-pink);">${tld}</span>`;
            if (path) htmlStr += `<span style="color: var(--text-muted);">${path}</span>`;

            htmlStr += `</div><ul style="list-style: none; padding: 0; margin: 0; font-size: 0.85rem;">`;

            if (protocol) {
                htmlStr += `<li style="margin-bottom: 0.5rem;"><strong style="color: var(--primary-light);">Protocol (${protocol}):</strong> Determines connection security.</li>`;
            }
            if (domain_name) {
                htmlStr += `<li style="margin-bottom: 0.5rem;"><strong style="color: var(--secondary);">Domain Name (${domain_name}):</strong> AI scans this core name for manipulation.</li>`;
            }
            if (tld) {
                htmlStr += `<li style="margin-bottom: 0.5rem;"><strong style="color: var(--accent-pink);">Extension (${tld}):</strong> Some extensions are high-risk indicators.</li>`;
            }
            if (path && path !== "/") {
                htmlStr += `<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-muted);">Path (...${path.substring(0, 10)}${path.length > 10 ? '...' : ''}):</strong> Directs to a specific resource.</li>`;
            }
            htmlStr += `</ul>`;

            anatomyContainer.innerHTML = htmlStr;
        }
    }
}

// --- Utils ---
function showLoader(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = 'flex';
        el.style.opacity = '1';
    }
}

function hideLoader(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// --- Dashboard History ---
async function loadDashboardHistory() {
    const container = document.getElementById('historyContainer');
    if (!container) return;

    const token = localStorage.getItem('token');
    if (!token) {
        container.innerHTML = `<div style="text-align:center; padding: 2rem; color: var(--warning);"><p>Session expired. Please log in again to view your history.</p></div>`;
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/history`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();

        if (res.ok) {
            // Update Score dynamically
            const scoreDisplay = document.querySelector('div[style*="font-size: 2.5rem"]');
            if (scoreDisplay) {
                scoreDisplay.innerHTML = `${data.score}<span style="font-size: 1rem; color: var(--text-muted);">%</span>`;
            }

            const container = document.getElementById('historyContainer');
            if (!container) return;

            if (!data.history || data.history.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; color: var(--text-muted); padding: 2rem;">
                        <ion-icon name="happy-outline" style="font-size: 2rem; margin-bottom: 0.5rem; color: var(--success);"></ion-icon>
                        <p>No recent scans. Your history is clean!</p>
                        <p style="font-size: 0.85rem; margin-top: 0.5rem; color: var(--primary-light);">Tip: Try scanning a suspicious email or text message to see how the AI works.</p>
                    </div>
                `;
                return;
            }

            let html = '';
            data.history.forEach(item => {
                let colorClass, icon, bg, border;
                if (item.risk_level === 'High Risk') {
                    colorClass = 'risk-high';
                    icon = 'warning';
                    bg = 'rgba(255,23,68,0.05)';
                    border = 'var(--danger)';
                } else if (item.risk_level === 'Medium Risk') {
                    colorClass = 'risk-medium';
                    icon = 'alert-circle';
                    bg = 'rgba(255,234,0,0.05)';
                    border = 'var(--warning)';
                } else {
                    colorClass = 'risk-low';
                    icon = 'checkmark-circle';
                    bg = 'rgba(0,255,118,0.05)';
                    border = 'var(--success)';
                }

                const title = item.content.length > 30 ? item.content.substring(0, 30) + '...' : item.content;
                const timeStr = new Date(item.timestamp).toLocaleString();

                html += `
                    <div style="padding: 1rem; background: ${bg}; border-left: 3px solid ${border}; border-radius: 4px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <strong>${title}</strong>
                            <span class="${colorClass}" style="font-size: 0.85rem; font-weight: bold;"><ion-icon name="${icon}"></ion-icon> ${item.risk_level}</span>
                        </div>
                        <p style="margin: 0; font-size: 0.85rem;">${item.scan_type} Scan &bull; ${timeStr}</p>
                    </div>
                `;
            });
            container.innerHTML = html;
        } else {
            console.error("API Error: ", data.error);
            const container = document.getElementById('historyContainer');
            if (container) {
                container.innerHTML = `<div style="text-align:center; padding: 2rem; color: var(--danger);"><ion-icon name="warning" style="font-size: 2rem;"></ion-icon><p>Failed to load profile history: ${data.error}</p></div>`;
            }
        }
    } catch (e) {
        console.error("Failed to load history", e);
        const container = document.getElementById('historyContainer');
        if (container) {
            container.innerHTML = `<div style="text-align:center; padding: 2rem; color: var(--danger);"><p>Network error while fetching history.</p></div>`;
        }
    }
}

// Auto-run if on dashboard
if (window.location.pathname.includes('dashboard.html')) {
    // Run immediately instead of waiting for DOMContentLoaded just in case
    setTimeout(loadDashboardHistory, 100);
}

// --- Global Chatbot Injection ---
document.addEventListener('DOMContentLoaded', () => {
    // Inject CSS for spinner
    const style = document.createElement('style');
    style.innerHTML = `
        .spin { animation: spin 2s linear infinite; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
    `;
    document.head.appendChild(style);

    // Inject Widget HTML
    const widgetHTML = `
    <div id="chatbotWidget" style="position: fixed; bottom: 2rem; right: 2rem; z-index: 1000; font-family: 'Outfit', sans-serif;">
        <button id="chatToggleBtn" onclick="toggleChat()" style="background: var(--primary); color: white; border: none; border-radius: 50%; width: 60px; height: 60px; box-shadow: 0 4px 15px rgba(94, 53, 177, 0.4); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; transition: transform 0.3s; z-index: 1001; position: relative;">
            <ion-icon name="chatbubbles-outline"></ion-icon>
        </button>

        <div id="chatWindow" style="display: none; position: absolute; bottom: 80px; right: 0; width: 350px; height: 500px; background: var(--bg-panel); border: 1px solid rgba(255,255,255,0.1); border-radius: var(--radius-md); box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; overflow: hidden; backdrop-filter: blur(20px);">
            <div style="background: linear-gradient(135deg, rgba(94, 53, 177, 0.8), rgba(0, 229, 255, 0.6)); padding: 1rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; align-items: center; gap: 0.5rem; color: white;">
                    <ion-icon name="shield-checkmark" style="font-size: 1.5rem;"></ion-icon>
                    <div>
                        <h4 style="margin: 0; font-size: 1.1rem;">CyberAura</h4>
                        <span style="font-size: 0.75rem; opacity: 0.8;">Women's Safety AI</span>
                    </div>
                </div>
                <button onclick="toggleChat()" style="background: transparent; border: none; color: white; font-size: 1.5rem; cursor: pointer;">
                    <ion-icon name="close"></ion-icon>
                </button>
            </div>
            <div id="chatMessages" style="flex: 1; padding: 1rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem;">
                <div style="background: rgba(94, 53, 177, 0.2); padding: 1rem; border-radius: 12px 12px 12px 0; border: 1px solid rgba(94, 53, 177, 0.3); max-width: 85%; align-self: flex-start;">
                    <p style="margin: 0; font-size: 0.95rem; color: var(--text-main);">Hi! I'm Aura, your AI safety companion. Ask me about online harassment, suspicious job offers, romance scams, or general cyber safety tips.</p>
                </div>
            </div>
            <div style="padding: 1rem; border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 0.5rem; background: rgba(0,0,0,0.2);">
                <input type="text" id="chatInput" placeholder="Type your question..." onkeypress="handleChatEnter(event)" style="flex: 1; padding: 0.8rem 1rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); color: white; font-family: inherit; font-size: 0.95rem; outline: none;">
                <button onclick="sendMessage()" style="background: var(--secondary); border: none; border-radius: 50%; width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; color: var(--bg-dark); cursor: pointer; transition: transform 0.2s;">
                    <ion-icon name="send" style="font-size: 1.2rem; transform: translateX(2px);"></ion-icon>
                </button>
            </div>
        </div>
    </div>`;

    document.body.insertAdjacentHTML('beforeend', widgetHTML);
});

// Global Chatbot Logic exposed to window
window.toggleChat = function () {
    const chatWindow = document.getElementById('chatWindow');
    const chatToggleBtn = document.getElementById('chatToggleBtn');
    if (chatWindow.style.display === 'none' || !chatWindow.style.display) {
        chatWindow.style.display = 'flex';
        chatToggleBtn.style.transform = 'scale(0.9)';
    } else {
        chatWindow.style.display = 'none';
        chatToggleBtn.style.transform = 'scale(1)';
    }
}

window.handleChatEnter = function (event) {
    if (event.key === 'Enter') {
        window.sendMessage();
    }
}

window.sendMessage = async function () {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';
    const chatMessages = document.getElementById('chatMessages');

    const userDiv = document.createElement('div');
    userDiv.style = "background: rgba(0, 229, 255, 0.2); padding: 1rem; border-radius: 12px 12px 0 12px; border: 1px solid rgba(0, 229, 255, 0.3); max-width: 85%; align-self: flex-end;";
    userDiv.innerHTML = `<p style="margin: 0; font-size: 0.95rem; color: #fff;">${msg}</p>`;
    chatMessages.appendChild(userDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const loaderDiv = document.createElement('div');
    loaderDiv.style = "align-self: flex-start; margin-left: 0.5rem; color: var(--text-muted); font-size: 0.8rem; display: flex; align-items: center; gap: 0.3rem;";
    loaderDiv.innerHTML = `<ion-icon class="spin" name="sync"></ion-icon> Aura is typing...`;
    chatMessages.appendChild(loaderDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${API_BASE}/chatbot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
            body: JSON.stringify({ message: msg })
        });
        const data = await response.json();
        chatMessages.removeChild(loaderDiv);

        const aiDiv = document.createElement('div');
        aiDiv.style = "background: rgba(94, 53, 177, 0.2); padding: 1rem; border-radius: 12px 12px 12px 0; border: 1px solid rgba(94, 53, 177, 0.3); max-width: 85%; align-self: flex-start;";
        const formattedReply = data.reply ? data.reply.replace(/\n/g, '<br>') : "I'm sorry, I'm having trouble connecting right now.";
        aiDiv.innerHTML = `<p style="margin: 0; font-size: 0.95rem; color: var(--text-main); line-height: 1.5;">${formattedReply}</p>`;
        chatMessages.appendChild(aiDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        console.error("Chat error:", error);
        chatMessages.removeChild(loaderDiv);
        const errDiv = document.createElement('div');
        errDiv.style = "color: var(--danger); font-size: 0.85rem; text-align: center;";
        errDiv.innerText = "Error connecting to Aura. Please try again later.";
        chatMessages.appendChild(errDiv);
    }
}
