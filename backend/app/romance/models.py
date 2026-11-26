from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class RomanceQuote(Base):
    __tablename__ = "romance_quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(Text, nullable=False)
    author = Column(String(120), nullable=False)
    book_title = Column(String(160), nullable=False)