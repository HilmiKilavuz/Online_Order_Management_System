// Configuration - Load from .env file
// For local development, update .env with your AWS Load Balancer DNS
const API_URL = `http://${window.ENV?.API_URL || 'localhost:5000'}`;

// State
let currentUser = null;
let authToken = null;

// DOM Elements
const welcomeSection = document.getElementById('welcomeSection');
const dashboardSection = document.getElementById('dashboardSection');
const loginCard = document.getElementById('loginCard');
const registerCard = document.getElementById('registerCard');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const showRegisterLink = document.getElementById('showRegister');
const showLoginLink = document.getElementById('showLogin');
const logoutBtn = document.getElementById('logoutBtn');
const apiStatus = document.getElementById('apiStatus');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkApiHealth();
    checkExistingSession();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    showRegisterLink.addEventListener('click', (e) => {
        e.preventDefault();
        showRegisterForm();
    });

    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        showLoginForm();
    });

    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    logoutBtn.addEventListener('click', handleLogout);

    const copyTokenBtn = document.getElementById('copyTokenBtn');
    if (copyTokenBtn) {
        copyTokenBtn.addEventListener('click', copyToken);
    }
}

// API Health Check
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();

        if (data.status === 'healthy') {
            updateApiStatus('healthy', 'API Connected');
        } else {
            updateApiStatus('warning', 'API Degraded');
        }
    } catch (error) {
        updateApiStatus('error', 'API Offline');
        console.error('API Health Check Failed:', error);
    }
}

function updateApiStatus(status, text) {
    const statusDot = apiStatus.querySelector('.status-dot');
    const statusText = apiStatus.querySelector('.status-text');

    statusText.textContent = text;

    if (status === 'healthy') {
        statusDot.style.background = '#10b981';
    } else if (status === 'warning') {
        statusDot.style.background = '#f59e0b';
    } else {
        statusDot.style.background = '#ef4444';
    }
}

// Check for existing session
function checkExistingSession() {
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('currentUser');

    if (savedToken && savedUser) {
        authToken = savedToken;
        currentUser = JSON.parse(savedUser);
        showDashboard();
    }
}

// Form Switching
function showRegisterForm() {
    loginCard.classList.add('hidden');
    registerCard.classList.remove('hidden');
}

function showLoginForm() {
    registerCard.classList.add('hidden');
    loginCard.classList.remove('hidden');
}

// Handle Registration
async function handleRegister(e) {
    e.preventDefault();

    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    const submitBtn = registerForm.querySelector('button[type="submit"]');
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Account created successfully! Please login.', 'success');
            registerForm.reset();
            showLoginForm();
        } else {
            showToast(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showToast('Network error. Please check your API URL.', 'error');
        console.error('Registration error:', error);
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

// Handle Login
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const submitBtn = loginForm.querySelector('button[type="submit"]');
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.token;
            currentUser = data.user;

            // Save to localStorage
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));

            showToast('Login successful!', 'success');
            loginForm.reset();
            showDashboard();
        } else {
            showToast(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showToast('Network error. Please check your API URL.', 'error');
        console.error('Login error:', error);
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

// Handle Logout
function handleLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');

    showToast('Logged out successfully', 'info');
    showWelcome();
}

// Show Dashboard
function showDashboard() {
    welcomeSection.classList.add('hidden');
    dashboardSection.classList.remove('hidden');

    // Populate user data
    document.getElementById('userName').textContent = currentUser.username;
    document.getElementById('userInitial').textContent = currentUser.username.charAt(0).toUpperCase();
    document.getElementById('profileUsername').textContent = currentUser.username;
    document.getElementById('profileEmail').textContent = currentUser.email;
    document.getElementById('profileId').textContent = currentUser.id;

    // Show token (truncated)
    const tokenDisplay = document.getElementById('tokenDisplay');
    if (authToken) {
        const truncatedToken = authToken.substring(0, 50) + '...';
        tokenDisplay.textContent = truncatedToken;
    }
}

// Show Welcome
function showWelcome() {
    dashboardSection.classList.add('hidden');
    welcomeSection.classList.remove('hidden');
    showLoginForm();
}

// Copy Token
function copyToken() {
    if (authToken) {
        navigator.clipboard.writeText(authToken).then(() => {
            showToast('Token copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy token', 'error');
        });
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 3000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Periodic health check
setInterval(checkApiHealth, 30000); // Check every 30 seconds
