const AUTH_API_PREFIX = "/auth";
const AUTH_TOKEN_KEY = "token";

const authScreen = document.getElementById("authScreen");
const appScreen = document.getElementById("appScreen");
const authError = document.getElementById("authError");
const tabLoginBtn = document.getElementById("tabLoginBtn");
const tabRegisterBtn = document.getElementById("tabRegisterBtn");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const logoutBtn = document.getElementById("logoutBtn");
const specialMenu = document.getElementById("specialMenu");
const currentUserBadge = document.getElementById("currentUserBadge");

const registerPasswordInput = document.getElementById("registerPassword");
const registerSubmitBtn = document.getElementById("registerSubmitBtn");
const toggleRegisterPasswordBtn = document.getElementById("toggleRegisterPassword");
const passwordRuleItems = document.querySelectorAll("#passwordRequirements .password-rule");

function showAuthError(message) {
    authError.textContent = message;
    authError.classList.remove("d-none");
}

function hideAuthError() {
    authError.textContent = "";
    authError.classList.add("d-none");
}

function switchAuthTab(mode) {
    hideAuthError();
    const isLogin = mode === "login";
    tabLoginBtn.classList.toggle("active", isLogin);
    tabRegisterBtn.classList.toggle("active", !isLogin);
    loginForm.classList.toggle("d-none", !isLogin);
    registerForm.classList.toggle("d-none", isLogin);
}

function evaluatePasswordRules(password) {
    const rules = {
        length: password.length >= 8,
        upper: /[A-Z]/.test(password),
        lower: /[a-z]/.test(password),
        number: /\d/.test(password),
        special: /[^A-Za-z0-9]/.test(password)
    };
    const allValid = Object.values(rules).every(Boolean);
    return { rules, allValid };
}

function updatePasswordChecklist() {
    if (!registerPasswordInput || !registerSubmitBtn) return;

    const { rules, allValid } = evaluatePasswordRules(registerPasswordInput.value);

    passwordRuleItems.forEach((item) => {
        const key = item.dataset.rule;
        const isMet = Boolean(rules[key]);
        const icon = item.querySelector("i");

        item.classList.toggle("valid", isMet);
        if (icon) {
            icon.className = isMet ? "bi bi-check-circle-fill" : "bi bi-circle";
        }
    });

    registerSubmitBtn.disabled = !allValid;
    registerPasswordInput.setCustomValidity(
        allValid ? "" : "A senha precisa atender a todos os requisitos."
    );
}

function enterApp(user) {
    hideAuthError();
    authScreen.classList.add("d-none");
    appScreen.classList.remove("d-none");

    if (currentUserBadge) {
        currentUserBadge.textContent = user.name;
    }

    if (specialMenu) {
        specialMenu.classList.toggle("d-none", !user.is_special);
    }

    if (typeof renderWeekStrip === "function") {
        renderWeekStrip();
    }

    if (typeof loadRoutineData === "function") {
        loadRoutineData();
    }

    if (user.is_special && typeof loadSpecialData === "function") {
        loadSpecialData();
    }
}

function exitApp() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    appScreen.classList.add("d-none");
    authScreen.classList.remove("d-none");

    if (specialMenu) {
        specialMenu.classList.add("d-none");
    }

    if (currentUserBadge) {
        currentUserBadge.textContent = "";
    }

    loginForm.reset();
    registerForm.reset();
    updatePasswordChecklist();
    switchAuthTab("login");
}

tabLoginBtn.addEventListener("click", () => switchAuthTab("login"));
tabRegisterBtn.addEventListener("click", () => switchAuthTab("register"));

if (registerPasswordInput) {
    registerPasswordInput.addEventListener("input", updatePasswordChecklist);
    updatePasswordChecklist();
}

if (toggleRegisterPasswordBtn && registerPasswordInput) {
    toggleRegisterPasswordBtn.addEventListener("click", () => {
        const isPassword = registerPasswordInput.type === "password";
        registerPasswordInput.type = isPassword ? "text" : "password";
        const icon = toggleRegisterPasswordBtn.querySelector("i");
        if (icon) {
            icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
        }
    });
}

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAuthError();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {
        const data = await apiRequest(`${AUTH_API_PREFIX}/login`, {
            method: "POST",
            body: JSON.stringify({ email, password })
        });

        localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
        enterApp(data.user);
    } catch (error) {
        showAuthError(error.message || "Não foi possível entrar.");
    }
});

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAuthError();

    const name = document.getElementById("registerName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;

    const { allValid } = evaluatePasswordRules(password);
    if (!allValid) {
        showAuthError("A senha precisa atender a todos os requisitos.");
        return;
    }

    try {
        const registered = await apiRequest(`${AUTH_API_PREFIX}/register`, {
            method: "POST",
            body: JSON.stringify({ name, email, password })
        });

        if (registered && registered.access_token && registered.user) {
            localStorage.setItem(AUTH_TOKEN_KEY, registered.access_token);
            enterApp(registered.user);
            return;
        }

        const loginData = await apiRequest(`${AUTH_API_PREFIX}/login`, {
            method: "POST",
            body: JSON.stringify({ email, password })
        });

        localStorage.setItem(AUTH_TOKEN_KEY, loginData.access_token);
        enterApp(loginData.user);
    } catch (error) {
        showAuthError(error.message || "Não foi possível criar a conta.");
    }
});

logoutBtn.addEventListener("click", () => {
    exitApp();
});

async function initAuth() {
    const token = localStorage.getItem(AUTH_TOKEN_KEY);
    if (!token) {
        exitApp();
        return;
    }

    try {
        const user = await apiRequest(`${AUTH_API_PREFIX}/me`);
        enterApp(user);
    } catch (error) {
        exitApp();
    }
}

initAuth();