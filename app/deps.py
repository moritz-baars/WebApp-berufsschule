from .db import SessionLocal
from typing import Generator, Optional
from fastapi import Depends, Request, HTTPException
from .models import User
from sqlalchemy.orm import Session

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:

    user_id = request.session.get("user_id")

    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    return user

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:

    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        request.session.clear()
        raise HTTPException(status_code=401)

    return user