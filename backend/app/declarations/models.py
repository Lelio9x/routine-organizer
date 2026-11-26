from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from app.core.database import Base


class Declaration(Base):
    __tablename__ = "declarations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    question = Column(String(255), nullable=False)
    expected_answer = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    is_unlocked = Column(Boolean, default=False, nullable=False)