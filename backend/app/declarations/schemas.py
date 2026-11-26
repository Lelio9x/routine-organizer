from typing import Optional

from pydantic import BaseModel, Field


class UnlockAttempt(BaseModel):
    answer: str = Field(min_length=1, max_length=120)


class DeclarationResponse(BaseModel):
    id: int
    question: str
    is_unlocked: bool
    content: Optional[str] = None


class UnlockResponse(BaseModel):
    unlocked: bool
    message: str
    declaration: DeclarationResponse