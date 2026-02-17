from sqlalchemy.orm import Session
from ..repositories import user_repo
from ..security import hash_password, verify_password

def register_user(db: Session, name: str, email: str, password: str):
    existing = user_repo.get_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")

    password_hash = hash_password(password)
    return user_repo.create_user(db, name, email, password_hash)


def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
