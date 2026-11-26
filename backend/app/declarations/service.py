import re
import unicodedata
from difflib import SequenceMatcher

from fastapi import status
from sqlalchemy.orm import Session

from app.declarations.models import Declaration
from app.declarations.schemas import DeclarationResponse, UnlockResponse
from app.errors import AppError


def _normalize_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    without_accents = "".join(
        ch for ch in decomposed if unicodedata.category(ch) != "Mn"
    )
    cleaned = re.sub(r"[^a-z0-9\s/]", " ", without_accents.lower())
    return " ".join(cleaned.split())


def _is_answer_valid(user_answer: str, expected_answers: str) -> bool:
    normalized_input = _normalize_text(user_answer)
    if not normalized_input:
        return False

    accepted_list = [_normalize_text(opt) for opt in expected_answers.split("|")]
    for expected in accepted_list:
        if not expected:
            continue
        if normalized_input == expected:
            return True
        has_digits = any(ch.isdigit() for ch in expected) or any(
            ch.isdigit() for ch in normalized_input
        )
        if not has_digits and len(expected) >= 5:
            similarity = SequenceMatcher(None, normalized_input, expected).ratio()
            if similarity >= 0.80:
                return True

    return False


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

    if not _is_answer_valid(answer, declaration.expected_answer):
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