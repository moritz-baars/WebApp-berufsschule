from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models import Event


def list_events(
    db: Session,
    q: Optional[str] = None,
    active_only: bool = True,
) -> List[Event]:
    query = db.query(Event)

    if active_only:
        query = query.filter(Event.is_active.is_(True))

    if q:
        q = q.strip()
        if q:
            like = f"%{q}%"
            # .ilike funktioniert in SQLite idR, falls es zickt: .like + lower() Lösung
            query = query.filter(or_(Event.title.ilike(like), Event.description.ilike(like)))

    # nullslast() ist nicht in jedem SQLite/SQLAlchemy Setup gleich zuverlässig
    # -> robust: erst nach "has starts_at" sortieren, dann starts_at, dann id
    query = query.order_by(
        (Event.starts_at.is_(None)).asc(),
        Event.starts_at.asc(),
        Event.id.desc()
    )

    return query.all()
