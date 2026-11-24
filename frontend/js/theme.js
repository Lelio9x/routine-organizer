const themeToggleBtn = document.getElementById("themeToggleBtn");
const htmlElement = document.documentElement;

function applyTheme(theme) {
    htmlElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem("theme", theme);
    themeToggleBtn.innerHTML = theme === "dark"
        ? '<i class="bi bi-sun"></i>'
        : '<i class="bi bi-moon-stars"></i>';
}

const savedTheme = localStorage.getItem("theme") || "light";
applyTheme(savedTheme);

themeToggleBtn.addEventListener("click", () => {
    const current = htmlElement.getAttribute("data-bs-theme");
    applyTheme(current === "dark" ? "light" : "dark");
});