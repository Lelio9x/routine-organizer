from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    task_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_minutes: int = Field(ge=0, le=1439)
    duration: int = Field(default=30, ge=5, le=1440)
    color: str = Field(default="coral", max_length=20)
    icon: str = Field(default="bi-star", max_length=50)


class InboxTaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    duration: int = Field(default=30, ge=5, le=1440)
    color: str = Field(default="coral", max_length=20)
    icon: str = Field(default="bi-star", max_length=50)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    task_date: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_minutes: Optional[int] = Field(default=None, ge=0, le=1439)
    duration: Optional[int] = Field(default=None, ge=5, le=1440)
    color: Optional[str] = Field(default=None, max_length=20)
    icon: Optional[str] = Field(default=None, max_length=50)
    is_completed: Optional[bool] = None


class ScheduleInboxRequest(BaseModel):
    task_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_minutes: int = Field(ge=0, le=1439)


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    task_date: Optional[str]
    start_minutes: Optional[int]
    duration: int
    color: str
    icon: str
    is_completed: bool
    is_inbox: bool