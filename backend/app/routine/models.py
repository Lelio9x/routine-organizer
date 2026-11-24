from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(120), nullable=False)
    task_date = Column(String(10), index=True, nullable=True)
    start_minutes = Column(Integer, nullable=True)
    duration = Column(Integer, default=30, nullable=False)
    color = Column(String(20), default="coral", nullable=False)
    icon = Column(String(50), default="bi-star", nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    is_inbox = Column(Boolean, default=False, nullable=False)