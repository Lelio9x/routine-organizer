const specialMenu = document.getElementById("specialMenu");
const roleToggleBtn = document.getElementById("roleToggleBtn");
let isSpecialUser = true;

roleToggleBtn.addEventListener("click", () => {
    isSpecialUser = !isSpecialUser;
    specialMenu.classList.toggle("d-none", !isSpecialUser);
    roleToggleBtn.textContent = isSpecialUser ? "Special Mode: ON" : "Special Mode: OFF";
});

const dateInput = document.getElementById("nextMeetingDate");
const countdownDays = document.getElementById("countdownDays");
dateInput.value = "2026-12-20";

function updateCountdown() {
    const target = new Date(dateInput.value + "T00:00:00");
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const diff = Math.ceil((target - today) / (1000 * 60 * 60 * 24));
    countdownDays.textContent = diff >= 0 ? diff : 0;
}

dateInput.addEventListener("change", updateCountdown);
updateCountdown();

const quizData = {
    question: "In which month do we celebrate our anniversary?",
    answer: "september",
    declaration: "Every day with you is my favorite part of the routine."
};

document.getElementById("quizQuestion").textContent = quizData.question;
document.getElementById("quizSubmitBtn").addEventListener("click", () => {
    const userAnswer = document.getElementById("quizAnswer").value.trim().toLowerCase();
    const resultBox = document.getElementById("quizResult");
    resultBox.classList.remove("d-none");

    if (userAnswer === quizData.answer) {
        resultBox.textContent = quizData.declaration;
    } else {
        resultBox.textContent = "Not quite! Try again.";
    }
});

const quotes = [
    { text: "Whatever our souls are made of, his and mine are the same.", author: "Emily Brontë" },
    { text: "You have bewitched me, body and soul.", author: "Jane Austen" },
    { text: "I fell in love the way you fall asleep: slowly, and then all at once.", author: "John Green" }
];

let quoteIndex = 0;

function renderQuote() {
    document.getElementById("romanceQuote").textContent = `"${quotes[quoteIndex].text}"`;
    document.getElementById("romanceAuthor").textContent = `— ${quotes[quoteIndex].author}`;
}

document.getElementById("nextQuoteBtn").addEventListener("click", () => {
    quoteIndex = (quoteIndex + 1) % quotes.length;
    renderQuote();
});

renderQuote();