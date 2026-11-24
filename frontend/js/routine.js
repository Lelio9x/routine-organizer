let selectedDate = "2026-11-24";
let currentView = "day";

let inboxTasks = [
    { id: 1, title: "Do Laundry", duration: 60, icon: "bi-basket", color: "blue" },
    { id: 2, title: "Do Homework", duration: 60, icon: "bi-book", color: "green" }
];

let routineTasks = [
    { id: 101, date: "2026-11-22", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: true },
    { id: 102, date: "2026-11-22", startMinutes: 1320, duration: 30, title: "Go to bed", icon: "bi-moon-fill", color: "blue", completed: true },
    { id: 103, date: "2026-11-23", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: true },
    { id: 104, date: "2026-11-23", startMinutes: 840, duration: 60, title: "Database Study", icon: "bi-database", color: "green", completed: true },
    { id: 105, date: "2026-11-23", startMinutes: 1320, duration: 30, title: "Go to bed", icon: "bi-moon-fill", color: "blue", completed: true },
    { id: 106, date: "2026-11-24", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: true },
    { id: 107, date: "2026-11-24", startMinutes: 495, duration: 30, title: "Yoga Workout", icon: "bi-heart-pulse", color: "blue", completed: true },
    { id: 108, date: "2026-11-24", startMinutes: 570, duration: 30, title: "Study Binary Trees", icon: "bi-diagram-3", color: "green", completed: false },
    { id: 109, date: "2026-11-24", startMinutes: 630, duration: 60, title: "Team Meeting", icon: "bi-people", color: "coral", completed: false },
    { id: 110, date: "2026-11-24", startMinutes: 1320, duration: 30, title: "Go to bed", icon: "bi-moon-fill", color: "blue", completed: false },
    { id: 111, date: "2026-11-25", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: false },
    { id: 112, date: "2026-11-25", startMinutes: 1320, duration: 30, title: "Go to bed", icon: "bi-moon-fill", color: "blue", completed: false },
    { id: 113, date: "2026-11-26", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: false },
    { id: 114, date: "2026-11-26", startMinutes: 1320, duration: 30, title: "Go to bed", icon: "bi-moon-fill", color: "blue", completed: false },
    { id: 115, date: "2026-11-27", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: false },
    { id: 116, date: "2026-11-28", startMinutes: 480, duration: 15, title: "Wake up", icon: "bi-sun-fill", color: "coral", completed: false }
];

function formatMinutes(total) {
    const hours = String(Math.floor(total / 60)).padStart(2, "0");
    const mins = String(total % 60).padStart(2, "0");
    return `${hours}:${mins}`;
}

function getWeekDates(dateStr) {
    const base = new Date(dateStr + "T00:00:00");
    const dayOfWeek = base.getDay();
    const sunday = new Date(base);
    sunday.setDate(base.getDate() - dayOfWeek);

    const names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const days = [];
    for (let i = 0; i < 7; i++) {
        const d = new Date(sunday);
        d.setDate(sunday.getDate() + i);
        const iso = d.toISOString().split("T")[0];
        days.push({ iso, name: names[i], dayNum: d.getDate() });
    }
    return days;
}

function selectDateAndDayView(isoDate) {
    selectedDate = isoDate;
    setView("day");
}

function setView(view) {
    currentView = view;
    document.querySelectorAll(".view-btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.view === view);
    });

    document.getElementById("dayView").classList.toggle("d-none", view !== "day");
    document.getElementById("weekView").classList.toggle("d-none", view !== "week");
    document.getElementById("monthView").classList.toggle("d-none", view !== "month");
    document.getElementById("weekStrip").classList.toggle("d-none", view === "month");

    renderAll();
}

function renderHeader() {
    const d = new Date(selectedDate + "T00:00:00");
    const monthName = d.toLocaleString("en-US", { month: "long" });
    const year = d.getFullYear();
    const day = d.getDate();

    document.getElementById("headerDateTitle").innerHTML = currentView === "day"
        ? `${day}. ${monthName} <span class="text-coral">${year}</span>`
        : `${monthName} <span class="text-coral">${year}</span>`;

    document.getElementById("taskDate").value = selectedDate;
}

function renderWeekStrip() {
    const strip = document.getElementById("weekStrip");
    const weekDays = getWeekDates(selectedDate);

    strip.innerHTML = weekDays.map(d => `
        <div class="day-item ${d.iso === selectedDate ? "active" : ""}" onclick="selectDateAndDayView('${d.iso}')">
            <small class="text-muted">${d.name}</small>
            <div class="day-num">${d.dayNum}</div>
        </div>
    `).join("");
}

function renderInbox() {
    const container = document.getElementById("inboxList");
    if (inboxTasks.length === 0) {
        container.innerHTML = `
            <div class="empty-inbox-state">
                <div class="empty-inbox-icon"><i class="bi bi-inboxes"></i></div>
                <h6 class="fw-bold mb-1">Your Unstructured Thoughts</h6>
                <p class="small text-muted mb-0">Capture tasks and thoughts as they come. Move them to your timeline when you are ready to schedule.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = inboxTasks.map(task => `
        <div class="inbox-card shadow-sm">
            <div class="d-flex align-items-center gap-3">
                <i class="bi ${task.icon} fs-5 text-secondary"></i>
                <div>
                    <small class="text-muted d-block">${task.duration} min</small>
                    <span class="fw-semibold">${task.title}</span>
                </div>
            </div>
            <button class="btn btn-sm btn-link text-coral fs-4 p-0" onclick="moveToRoutine(${task.id})">
                <i class="bi bi-plus"></i>
            </button>
        </div>
    `).join("");
}

function renderTimeline() {
    const container = document.getElementById("timelineList");
    const dayTasks = routineTasks
        .filter(t => t.date === selectedDate)
        .sort((a, b) => a.startMinutes - b.startMinutes);

    if (dayTasks.length === 0) {
        container.innerHTML = `<p class="text-center text-muted py-5 mb-0">No tasks scheduled for this day yet.</p>`;
        return;
    }

    let html = "";
    dayTasks.forEach((task, index) => {
        const startStr = formatMinutes(task.startMinutes);
        const endStr = formatMinutes(task.startMinutes + task.duration);
        const bgClass = task.completed ? "bg-completed" : `bg-${task.color}`;

        html += `
            <div class="timeline-item">
                <div class="time-col">${startStr}</div>
                <div class="icon-circle ${bgClass}">
                    <i class="bi ${task.icon} fs-5"></i>
                </div>
                <div class="flex-grow-1 ${task.completed ? "task-completed" : ""}">
                    <small class="text-muted d-block">${startStr} - ${endStr} (${task.duration} min)</small>
                    <div class="fw-semibold">${task.title}</div>
                </div>
                <button class="check-btn ${task.completed ? "checked" : ""}" onclick="toggleTask(${task.id})">
                    ${task.completed ? '<i class="bi bi-check"></i>' : ""}
                </button>
            </div>
        `;

        if (index < dayTasks.length - 1) {
            const gap = dayTasks[index + 1].startMinutes - (task.startMinutes + task.duration);
            if (gap > 0) {
                html += `<div class="free-time-gap"><i class="bi bi-clock me-1"></i>${gap} min of free time</div>`;
            }
        }
    });

    container.innerHTML = html;
}

function renderWeekView() {
    const container = document.getElementById("weekGridContainer");
    const weekDays = getWeekDates(selectedDate);
    const hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"];
    const baseHeight = 560;
    const minGapPx = 58;

    let maxRequiredHeight = baseHeight;

    const preparedDays = weekDays.map(day => {
        const tasks = routineTasks
            .filter(t => t.date === day.iso)
            .sort((a, b) => a.startMinutes - b.startMinutes);

        let nextAvailableTop = 35;
        const positionedTasks = tasks.map(t => {
            const clamped = Math.max(480, Math.min(1320, t.startMinutes));
            const idealTop = ((clamped - 480) / (1320 - 480)) * (baseHeight - 70) + 35;
            const actualTop = Math.max(idealTop, nextAvailableTop);
            nextAvailableTop = actualTop + minGapPx;
            return { ...t, topPx: actualTop };
        });

        if (nextAvailableTop > maxRequiredHeight) {
            maxRequiredHeight = nextAvailableTop + 10;
        }

        return { ...day, tasks: positionedTasks };
    });

    const hoursHtml = hours.map(h => `<div>${h}</div>`).join("");

    const colsHtml = preparedDays.map(day => {
        const nodesHtml = day.tasks.map(t => {
            const bgClass = t.completed ? "bg-completed" : `bg-${t.color}`;
            return `
                <div class="week-node ${t.completed ? "completed" : ""}" style="top: ${t.topPx}px;" onclick="selectDateAndDayView('${day.iso}')">
                    <div class="week-node-circle ${bgClass}">
                        <i class="bi ${t.icon}"></i>
                    </div>
                    <span class="week-node-label">${t.title}</span>
                </div>
            `;
        }).join("");

        return `
            <div class="week-day-col" style="height: ${maxRequiredHeight}px;">
                <div class="week-track-line"></div>
                ${nodesHtml}
            </div>
        `;
    }).join("");

    container.innerHTML = `
        <div class="week-grid">
            <div class="week-hours-col" style="height: ${maxRequiredHeight}px;">${hoursHtml}</div>
            ${colsHtml}
        </div>
    `;
}

function renderMonthView() {
    const container = document.getElementById("monthGridContainer");
    const base = new Date(selectedDate + "T00:00:00");
    const year = base.getFullYear();
    const month = base.getMonth();

    const firstDay = new Date(year, month, 1);
    const startOffset = firstDay.getDay();
    const gridStart = new Date(year, month, 1 - startOffset);

    const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        .map(w => `<div>${w}</div>`).join("");

    let cellsHtml = "";
    for (let i = 0; i < 35; i++) {
        const d = new Date(gridStart);
        d.setDate(gridStart.getDate() + i);
        const iso = d.toISOString().split("T")[0];
        const isCurrentMonth = d.getMonth() === month;
        const label = isCurrentMonth ? d.getDate() : `${d.toLocaleString("en-US", { month: "short" })} ${d.getDate()}`;

        const tasks = routineTasks
            .filter(t => t.date === iso)
            .sort((a, b) => a.startMinutes - b.startMinutes)
            .slice(0, 3);

        const tasksHtml = tasks.map(t => {
            const bgClass = t.completed ? "bg-completed" : `bg-${t.color}`;
            return `
                <div class="month-task-row ${t.completed ? "completed" : ""}">
                    <span class="month-dot ${bgClass}"><i class="bi ${t.icon}"></i></span>
                    <span class="fw-semibold">${t.title}</span>
                    <span class="text-muted">${formatMinutes(t.startMinutes)}</span>
                </div>
            `;
        }).join("");

        cellsHtml += `
            <div class="month-cell ${iso === selectedDate ? "active" : ""} ${!isCurrentMonth ? "opacity-50" : ""}" onclick="selectDateAndDayView('${iso}')">
                <div class="month-day-badge">${label}</div>
                ${tasksHtml}
            </div>
        `;
    }

    container.innerHTML = `
        <div class="month-weekdays">${weekdays}</div>
        <div class="month-grid">${cellsHtml}</div>
    `;
}

function renderAll() {
    renderHeader();
    renderWeekStrip();
    renderInbox();
    renderTimeline();
    renderWeekView();
    renderMonthView();
}

function toggleTask(id) {
    const task = routineTasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        renderAll();
    }
}

function moveToRoutine(id) {
    const index = inboxTasks.findIndex(t => t.id === id);
    if (index === -1) return;
    const item = inboxTasks.splice(index, 1)[0];
    routineTasks.push({
        id: Date.now(),
        date: selectedDate,
        startMinutes: 720,
        duration: item.duration,
        title: item.title,
        icon: item.icon,
        color: item.color,
        completed: false
    });
    renderAll();
}

document.querySelectorAll(".view-btn").forEach(btn => {
    btn.addEventListener("click", () => setView(btn.dataset.view));
});

document.getElementById("prevDateBtn").addEventListener("click", () => {
    const d = new Date(selectedDate + "T00:00:00");
    d.setDate(d.getDate() - (currentView === "month" ? 30 : currentView === "week" ? 7 : 1));
    selectedDate = d.toISOString().split("T")[0];
    renderAll();
});

document.getElementById("nextDateBtn").addEventListener("click", () => {
    const d = new Date(selectedDate + "T00:00:00");
    d.setDate(d.getDate() + (currentView === "month" ? 30 : currentView === "week" ? 7 : 1));
    selectedDate = d.toISOString().split("T")[0];
    renderAll();
});

document.getElementById("quickInboxForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("quickInboxInput");
    const title = input.value.trim();
    if (!title) return;

    inboxTasks.push({
        id: Date.now(),
        title,
        duration: 30,
        icon: "bi-circle",
        color: "coral"
    });
    input.value = "";
    renderInbox();
});

document.getElementById("addTaskForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const title = document.getElementById("taskTitle").value;
    const date = document.getElementById("taskDate").value;
    const timeValue = document.getElementById("taskTime").value;
    const duration = parseInt(document.getElementById("taskDuration").value, 10);
    const color = document.getElementById("taskColor").value;

    const [hours, mins] = timeValue.split(":").map(Number);
    const startMinutes = hours * 60 + mins;

    if (routineTasks.some(t => t.date === date && t.startMinutes === startMinutes)) {
        alert("Time conflict: another task is already scheduled at this time.");
        return;
    }

    routineTasks.push({
        id: Date.now(),
        date,
        startMinutes,
        duration,
        title,
        icon: "bi-star",
        color,
        completed: false
    });

    selectedDate = date;
    renderAll();
    bootstrap.Modal.getInstance(document.getElementById("addTaskModal")).hide();
    e.target.reset();
});

renderAll();