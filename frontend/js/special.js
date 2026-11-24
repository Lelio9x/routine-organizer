let declarationsList = [];
let currentDeclarationIndex = 0;
let romanceQuotes = [];
let currentQuoteIndex = 0;

async function loadSpecialData() {
    try {
        const [countdown, declarations, quotes] = await Promise.all([
            apiRequest("/countdown/"),
            apiRequest("/declarations/"),
            apiRequest("/romance/")
        ]);

        renderCountdown(countdown);
        declarationsList = declarations;
        currentDeclarationIndex = 0;
        renderDeclaration();

        romanceQuotes = quotes;
        currentQuoteIndex = 0;
        renderRomanceQuote();
    } catch (error) {
        console.error(error.message);
    }
}

function renderCountdown(data) {
    if (!data) return;
    document.getElementById("countdownTitle").textContent = data.title;
    document.getElementById("countdownDays").textContent = data.days_remaining;
    document.getElementById("nextMeetingDate").value = data.target_date;
}

function renderDeclaration() {
    const counter = document.getElementById("quizCounter");
    const questionEl = document.getElementById("quizQuestion");
    const inputArea = document.getElementById("quizInputArea");
    const resultEl = document.getElementById("quizResult");
    const answerInput = document.getElementById("quizAnswer");

    if (declarationsList.length === 0) {
        counter.textContent = "0 / 0";
        questionEl.textContent = "Nenhuma declaração disponível ainda.";
        inputArea.classList.add("d-none");
        resultEl.classList.add("d-none");
        return;
    }

    const item = declarationsList[currentDeclarationIndex];
    counter.textContent = `${currentDeclarationIndex + 1} / ${declarationsList.length}`;
    questionEl.textContent = item.question;
    answerInput.value = "";

    if (item.is_unlocked) {
        inputArea.classList.add("d-none");
        resultEl.textContent = item.content;
        resultEl.classList.remove("d-none");
    } else {
        inputArea.classList.remove("d-none");
        resultEl.classList.add("d-none");
    }
}

function renderRomanceQuote() {
    const quoteEl = document.getElementById("romanceQuote");
    const authorEl = document.getElementById("romanceAuthor");

    if (romanceQuotes.length === 0) {
        quoteEl.textContent = "Nenhuma citação disponível ainda.";
        authorEl.textContent = "";
        return;
    }

    const current = romanceQuotes[currentQuoteIndex];
    quoteEl.textContent = `"${current.quote}"`;
    authorEl.textContent = `— ${current.author}, ${current.book_title}`;
}

document.getElementById("nextMeetingDate").addEventListener("change", async (e) => {
    const target_date = e.target.value;
    if (!target_date) return;

    try {
        const updated = await apiRequest("/countdown/", {
            method: "PUT",
            body: JSON.stringify({ target_date })
        });
        renderCountdown(updated);
    } catch (error) {
        alert(error.message);
    }
});

document.getElementById("quizSubmitBtn").addEventListener("click", async () => {
    if (declarationsList.length === 0) return;

    const item = declarationsList[currentDeclarationIndex];
    const answer = document.getElementById("quizAnswer").value.trim();
    if (!answer) return;

    try {
        const response = await apiRequest(`/declarations/${item.id}/unlock`, {
            method: "POST",
            body: JSON.stringify({ answer })
        });

        const resultEl = document.getElementById("quizResult");
        if (response.unlocked) {
            declarationsList[currentDeclarationIndex] = response.declaration;
            renderDeclaration();
        } else {
            resultEl.textContent = response.message;
            resultEl.classList.remove("d-none");
        }
    } catch (error) {
        alert(error.message);
    }
});

document.getElementById("prevQuizBtn").addEventListener("click", () => {
    if (declarationsList.length === 0) return;
    currentDeclarationIndex = (currentDeclarationIndex - 1 + declarationsList.length) % declarationsList.length;
    renderDeclaration();
});

document.getElementById("nextQuizBtn").addEventListener("click", () => {
    if (declarationsList.length === 0) return;
    currentDeclarationIndex = (currentDeclarationIndex + 1) % declarationsList.length;
    renderDeclaration();
});

document.getElementById("nextQuoteBtn").addEventListener("click", () => {
    if (romanceQuotes.length === 0) return;
    currentQuoteIndex = (currentQuoteIndex + 1) % romanceQuotes.length;
    renderRomanceQuote();
});