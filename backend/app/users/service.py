from fastapi import status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.errors import AppError
from app.users.models import User
from app.users.schemas import UserLogin, UserRegister


def register_user(db: Session, payload: UserRegister) -> User:
    existing_username = db.query(User).filter(User.username == payload.username).first()
    if existing_username:
        raise AppError("Nome de usuário já está em uso", status.HTTP_409_CONFLICT)

    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise AppError("E-mail já cadastrado", status.HTTP_409_CONFLICT)

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_special=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: UserLogin) -> tuple[str, User]:
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise AppError("Usuário ou senha inválidos", status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(user.id, user.username, user.is_special)
    return token, user


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppError("Usuário não encontrado", status.HTTP_404_NOT_FOUND)
    return user