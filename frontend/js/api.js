const API_BASE_URL = "http://127.0.0.1:8000";

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