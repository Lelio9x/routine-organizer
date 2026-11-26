from sqlalchemy.orm import Session

from app.romance.models import RomanceQuote
from app.romance.schemas import RomanceQuoteCreate


def list_quotes(db: Session) -> list[RomanceQuote]:
    return db.query(RomanceQuote).all()


def create_quote(db: Session, payload: RomanceQuoteCreate) -> RomanceQuote:
    item = RomanceQuote(
        quote=payload.quote,
        author=payload.author,
        book_title=payload.book_title,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item