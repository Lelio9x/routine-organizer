from fastapi import status
from sqlalchemy.orm import Session

from app.core.text import normalize_answer
from app.declarations.models import Declaration
from app.declarations.schemas import DeclarationResponse, UnlockResponse
from app.errors import AppError


def _serialize(declaration: Declaration) -> DeclarationResponse:
    return DeclarationResponse(
        id=declaration.id,
        question=declaration.question,
        is_unlocked=declaration.is_unlocked,
        content=declaration.content if declaration.is_unlocked else None,
    )


def list_declarations(db: Session, user_id: int) -> list[DeclarationResponse]:
    items = db.query(Declaration).filter(Declaration.user_id == user_id).all()
    return [_serialize(item) for item in items]


def unlock_declaration(
    db: Session,
    user_id: int,
    declaration_id: int,
    answer: str,
) -> UnlockResponse:
    declaration = (
        db.query(Declaration)
        .filter(Declaration.id == declaration_id, Declaration.user_id == user_id)
        .first()
    )
    if not declaration:
        raise AppError("Declaração não encontrada", status.HTTP_404_NOT_FOUND)

    if declaration.is_unlocked:
        return UnlockResponse(
            unlocked=True,
            message="Declaração já desbloqueada",
            declaration=_serialize(declaration),
        )

    normalized_input = normalize_answer(answer)
    normalized_expected = normalize_answer(declaration.expected_answer)

    if normalized_input != normalized_expected:
        return UnlockResponse(
            unlocked=False,
            message="Resposta incorreta. Tente novamente.",
            declaration=_serialize(declaration),
        )

    declaration.is_unlocked = True
    db.commit()
    db.refresh(declaration)

    return UnlockResponse(
        unlocked=True,
        message="Declaração desbloqueada com sucesso",
        declaration=_serialize(declaration),
    )