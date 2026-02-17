from .db import SessionLocal
from typing import Generator, Optional
from fastapi import Depends, Request
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