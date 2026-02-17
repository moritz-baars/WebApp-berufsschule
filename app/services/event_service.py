from __future__ import annotations

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Event
from ..repositories import event_repo


def get_events_for_homepage(
    db: Session,
    q: Optional[str],
    active: int,
) -> List[Event]:

    active_only = (active == 1)

    events = event_repo.list_events(
        db=db,
        q=q,
        active_only=active_only
    )

    now = datetime.utcnow()

    # Business-Regel:
    # Zeige nur Events,
    # - die kein Datum haben ODER
    # - deren Startzeit in der Zukunft liegt
    filtered = [
        e for e in events
        if e.starts_at is None or e.starts_at >= now
    ]

    return filtered
