from fastapi import status
from sqlalchemy.orm import Session

from app.errors import AppError
from app.routine.binary_tree import BinaryTree
from app.routine.models import Task
from app.routine.scheduling import (
    MINUTES_IN_DAY,
    compute_free_slots,
    find_conflict,
    format_minutes,
)
from app.routine.schemas import (
    InboxTaskCreate,
    ScheduleInboxRequest,
    TaskCreate,
    TaskUpdate,
    validate_iso_date,
)


def _require_valid_date(value: str) -> str:
    try:
        return validate_iso_date(value)
    except ValueError as exc:
        raise AppError(str(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)


def _build_day_tree(db: Session, user_id: int, task_date: str) -> BinaryTree:
    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.task_date == task_date,
            Task.is_inbox.is_(False),
        )
        .all()
    )
    tree = BinaryTree()
    for task in tasks:
        if task.start_minutes is not None:
            tree.insert(task.start_minutes, task)
    return tree


def _to_composite_key(task_date: str, start_minutes: int) -> int:
    date_int = int(task_date.replace("-", ""))
    return date_int * 10000 + start_minutes


def _ensure_fits_in_day(start_minutes: int, duration: int) -> None:
    if start_minutes + duration > MINUTES_IN_DAY:
        raise AppError(
            "A tarefa não pode ultrapassar a meia-noite. "
            "Reduza a duração ou divida em duas tarefas.",
            status.HTTP_400_BAD_REQUEST,
        )


def _ensure_no_conflict(tree: BinaryTree, start_minutes: int, duration: int) -> None:
    conflict = find_conflict(tree, start_minutes, duration)
    if conflict is None:
        return

    conflict_start = format_minutes(conflict.start_minutes)
    conflict_end = format_minutes(conflict.start_minutes + conflict.duration)
    raise AppError(
        f'Conflito de horário com "{conflict.title}" ({conflict_start} - {conflict_end}).',
        status.HTTP_409_CONFLICT,
    )


def get_day_routine(db: Session, user_id: int, task_date: str) -> list[Task]:
    _require_valid_date(task_date)
    tree = _build_day_tree(db, user_id, task_date)
    return tree.in_order()


def get_free_time(db: Session, user_id: int, task_date: str) -> list[dict[str, int]]:
    _require_valid_date(task_date)
    tree = _build_day_tree(db, user_id, task_date)
    return compute_free_slots(tree.in_order())


def get_range_routine(db: Session, user_id: int, start_date: str, end_date: str) -> list[Task]:
    _require_valid_date(start_date)
    _require_valid_date(end_date)
    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.is_inbox.is_(False),
            Task.task_date >= start_date,
            Task.task_date <= end_date,
        )
        .all()
    )
    tree = BinaryTree()
    for task in tasks:
        if task.task_date and task.start_minutes is not None:
            composite_key = _to_composite_key(task.task_date, task.start_minutes)
            tree.insert(composite_key, task)
    return tree.in_order()


def search_task_by_time(db: Session, user_id: int, task_date: str, start_minutes: int) -> Task:
    _require_valid_date(task_date)
    tree = _build_day_tree(db, user_id, task_date)
    task = tree.search(start_minutes)
    if not task:
        raise AppError("Nenhuma tarefa agendada neste horário", status.HTTP_404_NOT_FOUND)
    return task


def create_routine_task(db: Session, user_id: int, payload: TaskCreate) -> Task:
    _ensure_fits_in_day(payload.start_minutes, payload.duration)
    tree = _build_day_tree(db, user_id, payload.task_date)
    _ensure_no_conflict(tree, payload.start_minutes, payload.duration)

    task = Task(
        user_id=user_id,
        title=payload.title,
        task_date=payload.task_date,
        start_minutes=payload.start_minutes,
        duration=payload.duration,
        color=payload.color,
        icon=payload.icon,
        is_completed=False,
        is_inbox=False,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, user_id: int, task_id: int, payload: TaskUpdate) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise AppError("Tarefa não encontrada", status.HTTP_404_NOT_FOUND)

    if task.is_inbox and (payload.task_date is not None or payload.start_minutes is not None):
        raise AppError(
            "Para agendar uma tarefa da caixa de entrada, use a ação de agendar.",
            status.HTTP_400_BAD_REQUEST,
        )

    if not task.is_inbox:
        new_date = payload.task_date if payload.task_date is not None else task.task_date
        new_minutes = payload.start_minutes if payload.start_minutes is not None else task.start_minutes
        new_duration = payload.duration if payload.duration is not None else task.duration

        schedule_changed = (
            new_date != task.task_date
            or new_minutes != task.start_minutes
            or new_duration != task.duration
        )
        if schedule_changed:
            _ensure_fits_in_day(new_minutes, new_duration)
            tree = _build_day_tree(db, user_id, new_date)
            if new_date == task.task_date:
                # A própria tarefa sai da árvore para não conflitar consigo mesma.
                tree.remove(task.start_minutes)
            _ensure_no_conflict(tree, new_minutes, new_duration)

    if payload.title is not None:
        task.title = payload.title
    if payload.task_date is not None:
        task.task_date = payload.task_date
    if payload.start_minutes is not None:
        task.start_minutes = payload.start_minutes
    if payload.duration is not None:
        task.duration = payload.duration
    if payload.color is not None:
        task.color = payload.color
    if payload.icon is not None:
        task.icon = payload.icon
    if payload.is_completed is not None:
        task.is_completed = payload.is_completed

    db.commit()
    db.refresh(task)
    return task


def toggle_task_completion(db: Session, user_id: int, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise AppError("Tarefa não encontrada", status.HTTP_404_NOT_FOUND)

    task.is_completed = not task.is_completed
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user_id: int, task_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise AppError("Tarefa não encontrada", status.HTTP_404_NOT_FOUND)

    # A árvore é reconstruída a cada requisição a partir do banco, então
    # apagar a linha já remove a tarefa da agenda.
    db.delete(task)
    db.commit()


def get_inbox_tasks(db: Session, user_id: int) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.is_inbox.is_(True))
        .all()
    )


def create_inbox_task(db: Session, user_id: int, payload: InboxTaskCreate) -> Task:
    task = Task(
        user_id=user_id,
        title=payload.title,
        task_date=None,
        start_minutes=None,
        duration=payload.duration,
        color=payload.color,
        icon=payload.icon,
        is_completed=False,
        is_inbox=True,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def schedule_inbox_task(
    db: Session,
    user_id: int,
    task_id: int,
    payload: ScheduleInboxRequest,
) -> Task:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id, Task.is_inbox.is_(True))
        .first()
    )
    if not task:
        raise AppError("Tarefa da caixa de entrada não encontrada", status.HTTP_404_NOT_FOUND)

    duration = payload.duration if payload.duration is not None else task.duration
    _ensure_fits_in_day(payload.start_minutes, duration)

    tree = _build_day_tree(db, user_id, payload.task_date)
    _ensure_no_conflict(tree, payload.start_minutes, duration)

    if payload.title is not None:
        task.title = payload.title
    if payload.color is not None:
        task.color = payload.color
    if payload.icon is not None:
        task.icon = payload.icon
    task.duration = duration
    task.task_date = payload.task_date
    task.start_minutes = payload.start_minutes
    task.is_inbox = False

    db.commit()
    db.refresh(task)
    return task
