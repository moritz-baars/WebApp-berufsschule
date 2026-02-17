from sqlalchemy.orm import Session
from ..models import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, name: str, email: str, password_hash: str):
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
