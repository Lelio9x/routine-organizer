from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_special_user
from app.countdown import service
from app.countdown.schemas import CountdownResponse, CountdownUpdate

router = APIRouter(prefix="/countdown", tags=["Countdown"])


@router.get("/", response_model=CountdownResponse)
def read_countdown(
    current_user: dict = Depends(require_special_user),
    db: Session = Depends(get_db),
):
    return service.get_countdown(db, current_user["user_id"])


@router.put("/", response_model=CountdownResponse)
def save_countdown(
    payload: CountdownUpdate,
    current_user: dict = Depends(require_special_user),
    db: Session = Depends(get_db),
):
    return service.update_countdown(db, current_user["user_id"], payload)