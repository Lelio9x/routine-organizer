from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
COLOR_PATTERN = r"^[a-z]{1,20}$"
ICON_PATTERN = r"^bi-[a-z0-9-]{1,46}$"


def validate_iso_date(value: str) -> str:
    """Rejeita datas que passam no formato mas não existem (ex.: 2026-13-45)."""
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError("Data inválida. Use o formato AAAA-MM-DD com uma data real.")
    return value


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=120)
    task_date: str = Field(pattern=DATE_PATTERN)
    start_minutes: int = Field(ge=0, le=1439)
    duration: int = Field(default=30, ge=5, le=1440)
    color: str = Field(default="coral", pattern=COLOR_PATTERN)
    icon: str = Field(default="bi-star", pattern=ICON_PATTERN)

    @field_validator("task_date")
    @classmethod
    def _check_date(cls, value: str) -> str:
        return validate_iso_date(value)


class InboxTaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=120)
    duration: int = Field(default=30, ge=5, le=1440)
    color: str = Field(default="coral", pattern=COLOR_PATTERN)
    icon: str = Field(default="bi-star", pattern=ICON_PATTERN)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    task_date: Optional[str] = Field(default=None, pattern=DATE_PATTERN)
    start_minutes: Optional[int] = Field(default=None, ge=0, le=1439)
    duration: Optional[int] = Field(default=None, ge=5, le=1440)
    color: Optional[str] = Field(default=None, pattern=COLOR_PATTERN)
    icon: Optional[str] = Field(default=None, pattern=ICON_PATTERN)
    is_completed: Optional[bool] = None

    @field_validator("task_date")
    @classmethod
    def _check_date(cls, value: Optional[str]) -> Optional[str]:
        return validate_iso_date(value) if value is not None else value


class ScheduleInboxRequest(BaseModel):
    """Agenda uma tarefa da caixa de entrada.

    Os campos opcionais permitem ajustar título, duração, cor e ícone na mesma
    chamada, para que o conflito de horário seja checado já com a duração final.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    task_date: str = Field(pattern=DATE_PATTERN)
    start_minutes: int = Field(ge=0, le=1439)
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    duration: Optional[int] = Field(default=None, ge=5, le=1440)
    color: Optional[str] = Field(default=None, pattern=COLOR_PATTERN)
    icon: Optional[str] = Field(default=None, pattern=ICON_PATTERN)

    @field_validator("task_date")
    @classmethod
    def _check_date(cls, value: str) -> str:
        return validate_iso_date(value)


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


class FreeSlotResponse(BaseModel):
    start_minutes: int
    end_minutes: int
    duration: int
