from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from ..models import Event


def list_events(
    db: Session,
    q: Optional[str] = None,
    active_only: bool = True,
    future_only: bool = False,   # <-- NEU
) -> List[Event]:
    query = db.query(Event)

    if active_only:
        query = query.filter(Event.is_active.is_(True))

    if future_only:
        now = datetime.utcnow()
        query = query.filter(
            or_(
                Event.starts_at.is_(None),
                Event.starts_at >= now
            )
        )

    if q:
        q = q.strip()
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    Event.title.ilike(like),
                    Event.description.ilike(like)
                )
            )

    query = query.order_by(
        (Event.starts_at.is_(None)).asc(),
        Event.starts_at.asc(),
        Event.id.desc()
    )

    return query.all()

def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

def list_all_events(db: Session) -> List[Event]:
    return db.query(Event).order_by(Event.id.desc()).all()