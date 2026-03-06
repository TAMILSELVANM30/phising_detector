// Auth API Service
const API_BASE = '/api';

async function register(e) {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
        const res = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            window.location.href = 'dashboard.html';
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert("Registration failed. Backend running?");
    }
}

async function login(e) {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            window.location.href = 'dashboard.html';
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert("Login failed. Backend running?");
    }
}

async function forgotPassword(e) {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();

    // Store email temporarily so we don't have to re-type it on the next page
    sessionStorage.setItem('resetEmail', email);

    try {
        const res = await fetch(`${API_BASE}/forgot-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        alert(data.message || data.error);
        if (res.ok) {
            window.location.href = 'reset_password.html';
        }
    } catch (err) {
        alert("Failed to send reset request.");
    }
}

async function resetPassword(e) {
    e.preventDefault();
    const email = document.getElementById('email').value.trim() || sessionStorage.getItem('resetEmail');
    const code = document.getElementById('code').value.trim();
    const new_password = document.getElementById('new_password').value;

    try {
        const res = await fetch(`${API_BASE}/reset-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, code, new_password })
        });
        const data = await res.json();
        alert(data.message || data.error);
        if (res.ok) {
            sessionStorage.removeItem('resetEmail');
            window.location.href = 'login.html';
        }
    } catch (err) {
        alert("Failed to reset password.");
    }
}

// Check logged in on restricted pages
function checkAuth() {
    // If URL has token (from OAuth), save it
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const name = params.get('name');
    if (token) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify({ name: name }));
        // Clean URL
        window.history.replaceState({}, document.title, window.location.pathname);
    }
}

// Check logged in on index
function updateNavbar() {
    const u = localStorage.getItem('user');
    const loginBtn = document.getElementById('navLoginBtn');
    const logoutBtn = document.getElementById('navLogoutBtn');
    if (loginBtn && logoutBtn) {
        if (u) {
            loginBtn.style.display = 'none';
            logoutBtn.style.display = 'inline-block';
        } else {
            loginBtn.style.display = 'inline-block';
            logoutBtn.style.display = 'none';
        }
    }
}

// Setup user UI in dashboard
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    updateNavbar();
    if (window.location.pathname.includes('dashboard') || window.location.pathname.includes('analyze') || window.location.pathname.includes('image_scan')) {
        const u = localStorage.getItem('user');
        if (!u) {
            window.location.href = 'login.html';
        } else {
            const userObj = JSON.parse(u);
            const greeting = document.getElementById('userNameGreeting');
            if (greeting) greeting.innerText = `Welcome back, ${userObj.name.split(' ')[0]}`;
        }
    }
});

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}
