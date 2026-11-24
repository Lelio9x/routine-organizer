from fastapi import status
from sqlalchemy.orm import Session

from app.errors import AppError
from app.routine.binary_tree import BinaryTree
from app.routine.models import Task
from app.routine.schemas import InboxTaskCreate, ScheduleInboxRequest, TaskCreate, TaskUpdate


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


def get_day_routine(db: Session, user_id: int, task_date: str) -> list[Task]:
    tree = _build_day_tree(db, user_id, task_date)
    return tree.in_order()


def get_range_routine(db: Session, user_id: int, start_date: str, end_date: str) -> list[Task]:
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
    tree = _build_day_tree(db, user_id, task_date)
    task = tree.search(start_minutes)
    if not task:
        raise AppError("No task scheduled at this time", status.HTTP_404_NOT_FOUND)
    return task


def create_routine_task(db: Session, user_id: int, payload: TaskCreate) -> Task:
    tree = _build_day_tree(db, user_id, payload.task_date)
    inserted = tree.insert(payload.start_minutes, payload)
    if not inserted:
        raise AppError(
            "Time conflict: another task is already scheduled at this time",
            status.HTTP_409_CONFLICT,
        )

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
        raise AppError("Task not found", status.HTTP_404_NOT_FOUND)

    new_date = payload.task_date if payload.task_date is not None else task.task_date
    new_minutes = payload.start_minutes if payload.start_minutes is not None else task.start_minutes

    if not task.is_inbox and new_date is not None and new_minutes is not None:
        schedule_changed = new_date != task.task_date or new_minutes != task.start_minutes
        if schedule_changed:
            target_tree = _build_day_tree(db, user_id, new_date)
            if new_date == task.task_date and task.start_minutes is not None:
                target_tree.remove(task.start_minutes)
            if not target_tree.insert(new_minutes, task):
                raise AppError(
                    "Time conflict: another task is already scheduled at this time",
                    status.HTTP_409_CONFLICT,
                )

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
        raise AppError("Task not found", status.HTTP_404_NOT_FOUND)

    task.is_completed = not task.is_completed
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user_id: int, task_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise AppError("Task not found", status.HTTP_404_NOT_FOUND)

    if not task.is_inbox and task.task_date and task.start_minutes is not None:
        tree = _build_day_tree(db, user_id, task.task_date)
        tree.remove(task.start_minutes)

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
        raise AppError("Inbox task not found", status.HTTP_404_NOT_FOUND)

    tree = _build_day_tree(db, user_id, payload.task_date)
    if not tree.insert(payload.start_minutes, task):
        raise AppError(
            "Time conflict: another task is already scheduled at this time",
            status.HTTP_409_CONFLICT,
        )

    task.task_date = payload.task_date
    task.start_minutes = payload.start_minutes
    task.is_inbox = False
    db.commit()
    db.refresh(task)
    return task