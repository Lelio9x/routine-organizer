from typing import Optional

from pydantic import BaseModel, Field


class CountdownUpdate(BaseModel):
    target_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)


class CountdownResponse(BaseModel):
    id: int
    title: str
    target_date: str
    days_remaining: int