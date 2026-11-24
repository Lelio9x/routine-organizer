from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.routine import service
from app.routine.schemas import (
    InboxTaskCreate,
    ScheduleInboxRequest,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter(prefix="/routine", tags=["Routine"])


@router.get("/day", response_model=list[TaskResponse])
def list_day_routine(
    date: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_day_routine(db, current_user["user_id"], date)


@router.get("/range", response_model=list[TaskResponse])
def list_range_routine(
    start_date: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_range_routine(db, current_user["user_id"], start_date, end_date)


@router.get("/search", response_model=TaskResponse)
def search_by_time(
    date: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    start_minutes: int = Query(ge=0, le=1439),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.search_task_by_time(db, current_user["user_id"], date, start_minutes)


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.create_routine_task(db, current_user["user_id"], payload)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.update_task(db, current_user["user_id"], task_id, payload)


@router.patch("/tasks/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.toggle_task_completion(db, current_user["user_id"], task_id)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service.delete_task(db, current_user["user_id"], task_id)


@router.get("/inbox", response_model=list[TaskResponse])
def list_inbox(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_inbox_tasks(db, current_user["user_id"])


@router.post("/inbox", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_inbox(
    payload: InboxTaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.create_inbox_task(db, current_user["user_id"], payload)


@router.post("/inbox/{task_id}/schedule", response_model=TaskResponse)
def schedule_inbox(
    task_id: int,
    payload: ScheduleInboxRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.schedule_inbox_task(db, current_user["user_id"], task_id, payload)