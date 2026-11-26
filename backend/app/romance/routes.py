from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_special_user
from app.romance import service
from app.romance.schemas import RomanceQuoteCreate, RomanceQuoteResponse

router = APIRouter(prefix="/romance", tags=["Romance"])


@router.get("/", response_model=list[RomanceQuoteResponse])
def get_quotes(
    current_user: dict = Depends(require_special_user),
    db: Session = Depends(get_db),
):
    return service.list_quotes(db)


@router.post("/", response_model=RomanceQuoteResponse, status_code=status.HTTP_201_CREATED)
def add_quote(
    payload: RomanceQuoteCreate,
    current_user: dict = Depends(require_special_user),
    db: Session = Depends(get_db),
):
    return service.create_quote(db, payload)