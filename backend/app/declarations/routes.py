from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_special_user
from app.declarations import service
from app.declarations.schemas import DeclarationResponse, UnlockAttempt, UnlockResponse

router = APIRouter(prefix="/declarations", tags=["Declarations"])


@router.get("/", response_model=list[DeclarationResponse])
def get_declarations(
    current_user: dict = Depends(require_special_user),
    db: Session = Depends(get_db),
):
    return service.list_declarations(db, current_user["user_id"])


@router.post("/{declaration_id}/unlock", response_model=UnlockResponse)
def try_unlock_declaration(
    declaration_id: int,
    payload: UnlockAttempt,
    current_user: dict = Depends(require_special_user),
    db: Session = Depends(get_db),
):
    return service.unlock_declaration(db, current_user["user_id"], declaration_id, payload.answer)