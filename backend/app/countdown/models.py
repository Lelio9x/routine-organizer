from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.database import Base


class Countdown(Base):
    __tablename__ = "countdowns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    title = Column(String(120), default="Until We Meet Again", nullable=False)
    target_date = Column(String(10), nullable=False)