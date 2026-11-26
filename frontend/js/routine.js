let selectedDate = formatDateISO(new Date());
let currentView = "day";
let editingTaskId = null;
let schedulingInboxId = null;

let inboxTasks = [];
let routineTasks = [];
const pendingToggles = new Set();

function formatDateISO(dateObj) {
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, "0");
    const day = String(dateObj.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function formatMinutes(total) {
    const hours = String(Math.floor(total / 60)).padStart(2, "0");
    const mins = String(total % 60).padStart(2, "0");
    return `${hours}:${mins}`;
}

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
}

function getWeekDates(dateStr) {
    const base = new Date(dateStr + "T00:00:00");
    const dayOfWeek = base.getDay();
    const sunday = new Date(base);
    sunday.setDate(base.getDate() - dayOfWeek);

    const names = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
    const days = [];
    for (let i = 0; i < 7; i++) {
        const d = new Date(sunday);
        d.setDate(sunday.getDate() + i);
        days.push({ iso: formatDateISO(d), name: names[i], dayNum: d.getDate() });
    }
    return days;
}

function getMonthRange(dateStr) {
    const base = new Date(dateStr + "T00:00:00");
    const firstDay = new Date(base.getFullYear(), base.getMonth(), 1);
    const gridStart = new Date(base.getFullYear(), base.getMonth(), 1 - firstDay.getDay());
    const gridEnd = new Date(gridStart);
    gridEnd.setDate(gridStart.getDate() + 34);
    return {
        start: formatDateISO(gridStart),
        end: formatDateISO(gridEnd)
    };
}

async function loadRoutineData() {
    try {
        const inboxPromise = apiRequest("/routine/inbox");
        let routinePromise;

        if (currentView === "day") {
            routinePromise = apiRequest(`/routine/day?date=${selectedDate}`);
        } else if (currentView === "week") {
            const weekDays = getWeekDates(selectedDate);
            routinePromise = apiRequest(
                `/routine/range?start_date=${weekDays[0].iso}&end_date=${weekDays[6].iso}`
            );
        } else {
            const range = getMonthRange(selectedDate);
            routinePromise = apiRequest(
                `/routine/range?start_date=${range.start}&end_date=${range.end}`
            );
        }

        const [loadedInbox, loadedRoutine] = await Promise.all([inboxPromise, routinePromise]);
        inboxTasks = loadedInbox;
        routineTasks = loadedRoutine;
        renderAll();
    } catch (error) {
        showNotification(error.message);
    }
}

function selectDateAndDayView(isoDate) {
    selectedDate = isoDate;
    setView("day");
}

function setView(view) {
    currentView = view;
    document.querySelectorAll(".view-btn[data-view]").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.view === view);
    });

    document.getElementById("dayView").classList.toggle("d-none", view !== "day");
    document.getElementById("weekView").classList.toggle("d-none", view !== "week");
    document.getElementById("monthView").classList.toggle("d-none", view !== "month");

    const weekStrip = document.getElementById("weekStrip");
    weekStrip.classList.remove("d-none", "d-flex", "d-lg-flex");
    if (view === "day") {
        weekStrip.classList.add("d-flex");
    } else if (view === "week") {
        weekStrip.classList.add("d-none", "d-lg-flex");
    } else {
        weekStrip.classList.add("d-none");
    }

    loadRoutineData();
}

function renderHeader() {
    const d = new Date(selectedDate + "T00:00:00");
    const monthName = capitalize(d.toLocaleString("pt-BR", { month: "long" }));
    const year = d.getFullYear();
    const day = d.getDate();

    document.getElementById("headerDateTitle").innerHTML = currentView === "day"
        ? `${day} de ${monthName} <span class="text-coral">${year}</span>`
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
    const countBadge = document.getElementById("inboxCountBadge");
    if (countBadge) {
        countBadge.textContent = inboxTasks.length;
    }

    const container = document.getElementById("inboxList");
    if (inboxTasks.length === 0) {
        container.innerHTML = `
            <div class="empty-inbox-state">
                <div class="empty-inbox-icon"><i class="bi bi-inboxes"></i></div>
                <h6 class="fw-bold mb-1">Seus Pensamentos Soltos</h6>
                <p class="small text-muted mb-0">Anote tarefas e ideias conforme surgirem. Mova para a linha do tempo quando estiver pronto para agendar.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = inboxTasks.map(task => `
        <div class="inbox-card shadow-sm">
            <div class="d-flex align-items-center gap-3 task-clickable">
                <i class="bi ${task.icon} fs-5 text-secondary"></i>
                <div class="task-info">
                    <small class="text-muted d-block">${task.duration} min</small>
                    <span class="fw-semibold">${task.title}</span>
                </div>
            </div>
            <button class="btn btn-sm btn-link text-coral fs-4 p-0" onclick="openScheduleInboxModal(${task.id})">
                <i class="bi bi-plus"></i>
            </button>
        </div>
    `).join("");
}

function renderTimeline() {
    const container = document.getElementById("timelineList");
    const dayTasks = routineTasks.filter(t => t.task_date === selectedDate);

    if (dayTasks.length === 0) {
        container.innerHTML = `<p class="text-center text-muted py-5 mb-0">Nenhuma tarefa agendada para este dia ainda.</p>`;
        return;
    }

    let html = "";
    dayTasks.forEach((task, index) => {
        const startStr = formatMinutes(task.start_minutes);
        const endStr = formatMinutes(task.start_minutes + task.duration);
        const bgClass = task.is_completed ? "bg-completed" : `bg-${task.color}`;

        html += `
            <div class="timeline-item" data-task-id="${task.id}">
                <div class="time-col">${startStr}</div>
                <div class="d-flex align-items-center gap-3 flex-grow-1 task-clickable" onclick="openEditTaskModal(${task.id})">
                    <div class="icon-circle ${bgClass}">
                        <i class="bi ${task.icon} fs-5"></i>
                    </div>
                    <div class="task-info flex-grow-1 ${task.is_completed ? "task-completed" : ""}">
                        <small class="text-muted d-block">${startStr} - ${endStr} (${task.duration} min)</small>
                        <div class="fw-semibold">${task.title}</div>
                    </div>
                </div>
                <button class="check-btn ${task.is_completed ? "checked" : ""}" onclick="toggleTask(${task.id})">
                    ${task.is_completed ? '<i class="bi bi-check"></i>' : ""}
                </button>
            </div>
        `;

        if (index < dayTasks.length - 1) {
            const gap = dayTasks[index + 1].start_minutes - (task.start_minutes + task.duration);
            if (gap > 0) {
                html += `<div class="free-time-gap"><i class="bi bi-clock me-1"></i>${gap} min de tempo livre</div>`;
            }
        }
    });

    container.innerHTML = html;
}

function updateTaskItemInDOM(task) {
    const itemEl = document.querySelector(`.timeline-item[data-task-id="${task.id}"]`);
    if (!itemEl) return;

    const circleEl = itemEl.querySelector(".icon-circle");
    const infoEl = itemEl.querySelector(".task-info");
    const checkBtn = itemEl.querySelector(".check-btn");

    circleEl.classList.remove("bg-completed", "bg-coral", "bg-blue", "bg-green");
    circleEl.classList.add(task.is_completed ? "bg-completed" : `bg-${task.color}`);

    infoEl.classList.toggle("task-completed", task.is_completed);
    checkBtn.classList.toggle("checked", task.is_completed);
    checkBtn.innerHTML = task.is_completed ? '<i class="bi bi-check"></i>' : "";
}

function renderWeekView() {
    const container = document.getElementById("weekGridContainer");
    const weekDays = getWeekDates(selectedDate);
    const hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"];
    const baseHeight = 560;
    const minGapPx = 58;

    let maxRequiredHeight = baseHeight;

    const preparedDays = weekDays.map(day => {
        const tasks = routineTasks.filter(t => t.task_date === day.iso);

        let nextAvailableTop = 35;
        const positionedTasks = tasks.map(t => {
            const clamped = Math.max(480, Math.min(1320, t.start_minutes));
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

    const mobileHeaderHtml = preparedDays.map(day => `
        <div class="week-mobile-day ${day.iso === selectedDate ? "active" : ""}" onclick="selectDateAndDayView('${day.iso}')">
            <small class="text-muted">${day.name}</small>
            <strong>${day.dayNum}</strong>
        </div>
    `).join("");

    const colsHtml = preparedDays.map(day => {
        const nodesHtml = day.tasks.map(t => {
            const bgClass = t.is_completed ? "bg-completed" : `bg-${t.color}`;
            return `
                <div class="week-node ${t.is_completed ? "completed" : ""}" style="top: ${t.topPx}px;" onclick="selectDateAndDayView('${day.iso}')">
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
        <div class="week-grid-mobile-header d-lg-none">
            <div></div>
            ${mobileHeaderHtml}
        </div>
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
    const gridStart = new Date(year, month, 1 - firstDay.getDay());

    const weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        .map(w => `<div>${w}</div>`).join("");

    let cellsHtml = "";
    for (let i = 0; i < 35; i++) {
        const d = new Date(gridStart);
        d.setDate(gridStart.getDate() + i);
        const iso = formatDateISO(d);
        const isCurrentMonth = d.getMonth() === month;
        const shortMonth = capitalize(d.toLocaleString("pt-BR", { month: "short" }).replace(".", ""));
        const label = isCurrentMonth ? d.getDate() : `${d.getDate()} ${shortMonth}`;

        const tasks = routineTasks
            .filter(t => t.task_date === iso)
            .slice(0, 3);

        const tasksHtml = tasks.map(t => {
            const bgClass = t.is_completed ? "bg-completed" : `bg-${t.color}`;
            return `
                <div class="month-task-row ${t.is_completed ? "completed" : ""}">
                    <span class="month-dot ${bgClass}"><i class="bi ${t.icon}"></i></span>
                    <span class="fw-semibold">${t.title}</span>
                    <span class="text-muted">${formatMinutes(t.start_minutes)}</span>
                </div>
            `;
        }).join("");

        cellsHtml += `
            <div class="month-cell ${iso === selectedDate ? "active" : ""} ${!isCurrentMonth ? "opacity-50" : ""}" onclick="selectDateAndDayView('${iso}')">
                <div class="month-day-badge">${label}</div>
                <div class="month-cell-tasks">${tasksHtml}</div>
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

    if (currentView === "day") {
        renderTimeline();
    } else if (currentView === "week") {
        renderWeekView();
    } else {
        renderMonthView();
    }
}

async function toggleTask(id) {
    if (pendingToggles.has(id)) return;
    const task = routineTasks.find(t => t.id === id);
    if (!task) return;

    pendingToggles.add(id);
    const previousState = task.is_completed;
    task.is_completed = !previousState;
    updateTaskItemInDOM(task);

    try {
        const updated = await apiRequest(`/routine/tasks/${id}/toggle`, { method: "PATCH" });
        task.is_completed = updated.is_completed;
        updateTaskItemInDOM(task);
    } catch (error) {
        task.is_completed = previousState;
        updateTaskItemInDOM(task);
        showNotification(error.message);
    } finally {
        pendingToggles.delete(id);
    }
}

function setIconSelectValue(iconValue) {
    const iconSelect = document.getElementById("taskIcon");
    const hasIcon = Array.from(iconSelect.options).some(opt => opt.value === iconValue);
    iconSelect.value = hasIcon ? iconValue : "bi-star";
}

function openNewTaskModal() {
    editingTaskId = null;
    schedulingInboxId = null;
    document.getElementById("addTaskForm").reset();
    document.getElementById("taskDate").value = selectedDate;
    document.getElementById("taskDuration").value = 30;
    document.getElementById("taskModalTitle").textContent = "Nova Tarefa";
    document.getElementById("saveTaskBtn").textContent = "Adicionar à Rotina";
    document.getElementById("deleteTaskBtn").classList.add("d-none");

    bootstrap.Modal.getOrCreateInstance(document.getElementById("addTaskModal")).show();
}

function openEditTaskModal(id) {
    const task = routineTasks.find(t => t.id === id);
    if (!task) return;

    editingTaskId = id;
    schedulingInboxId = null;
    document.getElementById("taskTitle").value = task.title;
    document.getElementById("taskDate").value = task.task_date;
    document.getElementById("taskTime").value = formatMinutes(task.start_minutes);
    document.getElementById("taskDuration").value = task.duration;
    document.getElementById("taskColor").value = task.color;
    setIconSelectValue(task.icon);

    document.getElementById("taskModalTitle").textContent = "Editar Tarefa";
    document.getElementById("saveTaskBtn").textContent = "Salvar Alterações";
    document.getElementById("deleteTaskBtn").classList.remove("d-none");

    bootstrap.Modal.getOrCreateInstance(document.getElementById("addTaskModal")).show();
}

function openScheduleInboxModal(id) {
    const task = inboxTasks.find(t => t.id === id);
    if (!task) return;

    editingTaskId = null;
    schedulingInboxId = id;
    document.getElementById("taskTitle").value = task.title;
    document.getElementById("taskDate").value = selectedDate;
    document.getElementById("taskTime").value = "12:00";
    document.getElementById("taskDuration").value = task.duration;
    document.getElementById("taskColor").value = task.color;
    setIconSelectValue(task.icon);

    document.getElementById("taskModalTitle").textContent = "Agendar Tarefa";
    document.getElementById("saveTaskBtn").textContent = "Mover para a Rotina";
    document.getElementById("deleteTaskBtn").classList.remove("d-none");

    bootstrap.Modal.getOrCreateInstance(document.getElementById("addTaskModal")).show();
}

document.querySelectorAll(".view-btn[data-view]").forEach(btn => {
    btn.addEventListener("click", () => setView(btn.dataset.view));
});

document.getElementById("prevDateBtn").addEventListener("click", () => {
    const d = new Date(selectedDate + "T00:00:00");
    d.setDate(d.getDate() - (currentView === "month" ? 30 : currentView === "week" ? 7 : 1));
    selectedDate = formatDateISO(d);
    loadRoutineData();
});

document.getElementById("nextDateBtn").addEventListener("click", () => {
    const d = new Date(selectedDate + "T00:00:00");
    d.setDate(d.getDate() + (currentView === "month" ? 30 : currentView === "week" ? 7 : 1));
    selectedDate = formatDateISO(d);
    loadRoutineData();
});

document.getElementById("quickInboxForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("quickInboxInput");
    const title = input.value.trim();
    if (!title) return;

    try {
        await apiRequest("/routine/inbox", {
            method: "POST",
            body: JSON.stringify({
                title,
                duration: 30,
                color: "coral",
                icon: "bi-star"
            })
        });
        input.value = "";
        await loadRoutineData();
    } catch (error) {
        showNotification(error.message);
    }
});

document.getElementById("deleteTaskBtn").addEventListener("click", async () => {
    const targetId = editingTaskId ?? schedulingInboxId;
    if (targetId === null) return;

    try {
        await apiRequest(`/routine/tasks/${targetId}`, { method: "DELETE" });
        editingTaskId = null;
        schedulingInboxId = null;
        bootstrap.Modal.getOrCreateInstance(document.getElementById("addTaskModal")).hide();
        await loadRoutineData();
    } catch (error) {
        showNotification(error.message);
    }
});

document.getElementById("addTaskForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("taskTitle").value.trim();
    const task_date = document.getElementById("taskDate").value;
    const timeValue = document.getElementById("taskTime").value;
    const duration = parseInt(document.getElementById("taskDuration").value, 10);
    const color = document.getElementById("taskColor").value;
    const icon = document.getElementById("taskIcon").value;

    const [hours, mins] = timeValue.split(":").map(Number);
    const start_minutes = hours * 60 + mins;

    try {
        if (schedulingInboxId !== null) {
            await apiRequest(`/routine/inbox/${schedulingInboxId}/schedule`, {
                method: "POST",
                body: JSON.stringify({ task_date, start_minutes })
            });
            await apiRequest(`/routine/tasks/${schedulingInboxId}`, {
                method: "PUT",
                body: JSON.stringify({ title, duration, color, icon })
            });
            schedulingInboxId = null;
        } else if (editingTaskId !== null) {
            await apiRequest(`/routine/tasks/${editingTaskId}`, {
                method: "PUT",
                body: JSON.stringify({ title, task_date, start_minutes, duration, color, icon })
            });
            editingTaskId = null;
        } else {
            await apiRequest("/routine/tasks", {
                method: "POST",
                body: JSON.stringify({ title, task_date, start_minutes, duration, color, icon })
            });
        }

        selectedDate = task_date;
        bootstrap.Modal.getOrCreateInstance(document.getElementById("addTaskModal")).hide();
        e.target.reset();
        await loadRoutineData();
    } catch (error) {
        showNotification(error.message);
    }
});