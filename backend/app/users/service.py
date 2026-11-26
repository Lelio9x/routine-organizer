import re

from fastapi import status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.declarations.models import Declaration
from app.errors import AppError
from app.users.models import User
from app.users.schemas import UserLogin, UserRegister


def _validate_password_strength(password: str) -> None:
    has_min_length = len(password) >= 8
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_number = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    if not all([has_min_length, has_upper, has_lower, has_number, has_special]):
        raise AppError(
            "A senha deve ter no mínimo 8 caracteres, incluindo letra maiúscula, minúscula, número e símbolo.",
            status.HTTP_400_BAD_REQUEST,
        )


def register_user(db: Session, payload: UserRegister) -> User:
    _validate_password_strength(payload.password)

    normalized_email = payload.email.strip().lower()
    cleaned_name = payload.name.strip()

    existing_email = db.query(User).filter(User.email == normalized_email).first()
    if existing_email:
        raise AppError("E-mail já cadastrado", status.HTTP_409_CONFLICT)

    user = User(
        name=cleaned_name,
        email=normalized_email,
        password_hash=hash_password(payload.password),
        is_special=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: UserLogin) -> tuple[str, User]:
    normalized_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise AppError("E-mail ou senha inválidos", status.HTTP_401_UNAUTHORIZED)

    if user.is_special:
        (
            db.query(Declaration)
            .filter(Declaration.user_id == user.id)
            .update({"is_unlocked": False})
        )
        db.commit()

    token = create_access_token(user.id, user.name, user.is_special)
    return token, user


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppError("Usuário não encontrado", status.HTTP_404_NOT_FOUND)
    return user