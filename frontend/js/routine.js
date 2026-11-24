let inboxTasks = [
    { id: 1, title: "Do Laundry", duration: 60, icon: "bi-basket", color: "blue" },
    { id: 2, title: "Do Homework", duration: 60, icon: "bi-book", color: "green" },
    { id: 3, title: "Go for a Run", duration: 45, icon: "bi-lightning", color: "coral" }
];

let routineTasks = [
    { id: 101, startMinutes: 480, duration: 15, title: "Rise and Shine", icon: "bi-alarm", color: "coral", completed: true },
    { id: 102, startMinutes: 495, duration: 30, title: "Yoga Workout", icon: "bi-heart-pulse", color: "blue", completed: true },
    { id: 103, startMinutes: 570, duration: 30, title: "Study Binary Trees", icon: "bi-diagram-3", color: "green", completed: false },
    { id: 104, startMinutes: 630, duration: 60, title: "Team Meeting", icon: "bi-people", color: "coral", completed: false }
];

function formatMinutes(total) {
    const hours = String(Math.floor(total / 60)).padStart(2, "0");
    const mins = String(total % 60).padStart(2, "0");
    return `${hours}:${mins}`;
}

function renderInbox() {
    const container = document.getElementById("inboxList");
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
    routineTasks.sort((a, b) => a.startMinutes - b.startMinutes);

    let html = "";
    routineTasks.forEach((task, index) => {
        const startStr = formatMinutes(task.startMinutes);
        const endStr = formatMinutes(task.startMinutes + task.duration);

        html += `
            <div class="timeline-item">
                <div class="time-col">${startStr}</div>
                <div class="icon-circle bg-${task.color}">
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

        if (index < routineTasks.length - 1) {
            const gap = routineTasks[index + 1].startMinutes - (task.startMinutes + task.duration);
            if (gap > 0) {
                html += `<div class="free-time-gap"><i class="bi bi-clock me-1"></i>${gap} min of free time</div>`;
            }
        }
    });

    container.innerHTML = html;
}

function toggleTask(id) {
    const task = routineTasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        renderTimeline();
    }
}

function moveToRoutine(id) {
    const index = inboxTasks.findIndex(t => t.id === id);
    if (index === -1) return;
    const item = inboxTasks.splice(index, 1)[0];
    routineTasks.push({
        id: Date.now(),
        startMinutes: 720,
        duration: item.duration,
        title: item.title,
        icon: item.icon,
        color: item.color,
        completed: false
    });
    renderInbox();
    renderTimeline();
}

document.getElementById("addTaskForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const title = document.getElementById("taskTitle").value;
    const timeValue = document.getElementById("taskTime").value;
    const duration = parseInt(document.getElementById("taskDuration").value, 10);
    const color = document.getElementById("taskColor").value;

    const [hours, mins] = timeValue.split(":").map(Number);
    const startMinutes = hours * 60 + mins;

    if (routineTasks.some(t => t.startMinutes === startMinutes)) {
        alert("Time conflict: another task is already scheduled at this time.");
        return;
    }

    routineTasks.push({
        id: Date.now(),
        startMinutes,
        duration,
        title,
        icon: "bi-star",
        color,
        completed: false
    });

    renderTimeline();
    bootstrap.Modal.getInstance(document.getElementById("addTaskModal")).hide();
    e.target.reset();
});

renderInbox();
renderTimeline();