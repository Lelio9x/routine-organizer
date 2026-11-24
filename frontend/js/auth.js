function showAuthError(message) {
    const box = document.getElementById("authError");
    box.textContent = message;
    box.classList.remove("d-none");
}

function hideAuthError() {
    document.getElementById("authError").classList.add("d-none");
}

function showAuthScreen() {
    document.getElementById("authScreen").classList.remove("d-none");
    document.getElementById("appScreen").classList.add("d-none");
}

async function enterApp(user) {
    document.getElementById("authScreen").classList.add("d-none");
    document.getElementById("appScreen").classList.remove("d-none");
    document.getElementById("currentUserBadge").textContent = user.username;

    const specialMenu = document.getElementById("specialMenu");
    if (user.is_special) {
        specialMenu.classList.remove("d-none");
        await loadSpecialData();
    } else {
        specialMenu.classList.add("d-none");
    }

    await loadRoutineData();
}

document.getElementById("tabLoginBtn").addEventListener("click", () => {
    hideAuthError();
    document.getElementById("tabLoginBtn").classList.add("active");
    document.getElementById("tabRegisterBtn").classList.remove("active");
    document.getElementById("loginForm").classList.remove("d-none");
    document.getElementById("registerForm").classList.add("d-none");
});

document.getElementById("tabRegisterBtn").addEventListener("click", () => {
    hideAuthError();
    document.getElementById("tabRegisterBtn").classList.add("active");
    document.getElementById("tabLoginBtn").classList.remove("active");
    document.getElementById("registerForm").classList.remove("d-none");
    document.getElementById("loginForm").classList.add("d-none");
});

document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAuthError();

    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {
        const data = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({ username, password })
        });
        setSession(data.access_token, data.user);
        e.target.reset();
        await enterApp(data.user);
    } catch (error) {
        showAuthError(error.message);
    }
});

document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAuthError();

    const username = document.getElementById("registerUsername").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;

    try {
        await apiRequest("/auth/register", {
            method: "POST",
            body: JSON.stringify({ username, email, password })
        });

        const loginData = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({ username, password })
        });
        setSession(loginData.access_token, loginData.user);
        e.target.reset();
        await enterApp(loginData.user);
    } catch (error) {
        showAuthError(error.message);
    }
});

document.getElementById("logoutBtn").addEventListener("click", () => {
    clearSession();
    showAuthScreen();
});

async function initializeApp() {
    const token = getToken();
    if (!token) {
        showAuthScreen();
        return;
    }

    try {
        const user = await apiRequest("/auth/me");
        setSession(token, user);
        await enterApp(user);
    } catch (error) {
        clearSession();
        showAuthScreen();
    }
}

initializeApp();