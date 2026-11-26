const IS_LOCAL =
    window.location.protocol === "file:" ||
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost";

const API_BASE_URL = IS_LOCAL
    ? "http://127.0.0.1:8000"
    : "https://routine-organizer-1.onrender.com";

function getToken() {
    return localStorage.getItem("auth_token");
}

function setSession(token, user) {
    localStorage.setItem("auth_token", token);
    localStorage.setItem("auth_user", JSON.stringify(user));
}

function clearSession() {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_user");
}

function getStoredUser() {
    const raw = localStorage.getItem("auth_user");
    return raw ? JSON.parse(raw) : null;
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (response.status === 204) {
        return null;
    }

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        if (response.status === 401 && endpoint !== "/auth/login") {
            clearSession();
            if (typeof showAuthScreen === "function") {
                showAuthScreen();
            }
        }
        throw new Error(data.detail || "Request failed");
    }

    return data;
}

function showNotification(message, title = "Atenção", type = "error") {
    const modalEl = document.getElementById("feedbackModal");
    if (!modalEl) return;

    const titleEl = document.getElementById("feedbackModalTitle");
    const messageEl = document.getElementById("feedbackModalMessage");
    const iconBox = document.getElementById("feedbackModalIcon");

    titleEl.textContent = title;
    messageEl.textContent = message;

    iconBox.classList.remove("feedback-error", "feedback-success");
    if (type === "success") {
        iconBox.classList.add("feedback-success");
        iconBox.innerHTML = '<i class="bi bi-check-lg"></i>';
    } else {
        iconBox.classList.add("feedback-error");
        iconBox.innerHTML = '<i class="bi bi-exclamation-triangle-fill"></i>';
    }

    bootstrap.Modal.getOrCreateInstance(modalEl).show();
}