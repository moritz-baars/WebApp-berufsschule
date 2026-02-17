from __future__ import annotations

from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Event
from ..repositories import event_repo, booking_repo


def get_events_for_homepage(
    db: Session,
    q: Optional[str],
    active: int,
):
    events = event_repo.list_events(
        db=db,
        q=q,
        active_only=(active == 1),
        future_only=True
    )

    booked_map = booking_repo.count_bookings_grouped_by_event(db)

    # map: event_id -> freie Plätze (oder None wenn unbegrenzt/kein Limit)
    free_map: Dict[int, Optional[int]] = {}

    for e in events:
        if e.max_participants and e.max_participants > 0:
            booked = booked_map.get(e.id, 0)
            free = max(e.max_participants - booked, 0)
            free_map[e.id] = free
        else:
            free_map[e.id] = None

    return events, free_map


def get_all_events_for_admin(db: Session) -> List[Event]:
    # Hier wäre später Platz für Admin-spezifische Regeln
    # z.B. auch inaktive und vergangene Events anzeigen
    return event_repo.list_all_events(db)
