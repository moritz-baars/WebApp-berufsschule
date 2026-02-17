from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Event, Booking
from ..repositories import event_repo, booking_repo

class AdminEventError(Exception):
    pass

def list_events(db: Session) -> List[Event]:
    # Admin darf alles sehen (auch vergangene/inaktive)
    return event_repo.list_all_events(db)

def get_event_detail(db: Session, event_id: int) -> tuple[Event, List[Booking]]:
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        raise AdminEventError("Event nicht gefunden.")
    attendees = booking_repo.list_attendees_for_event(db, event_id)
    return event, attendees

def _parse_datetime_local(value: Optional[str]) -> Optional[datetime]:
    # HTML datetime-local: "YYYY-MM-DDTHH:MM"
    if not value:
        return None
    return datetime.fromisoformat(value)

def create_event(db: Session, form: dict) -> Event:
    data = {
        "title": form["title"].strip(),
        "description": (form.get("description") or "").strip() or None,
        "location": (form.get("location") or "").strip() or None,
        "starts_at": _parse_datetime_local(form.get("starts_at")),
        "ends_at": _parse_datetime_local(form.get("ends_at")),
        "max_participants": int(form.get("max_participants") or 0),
        "is_active": True if form.get("is_active") == "1" else False,
    }
    if not data["title"]:
        raise AdminEventError("Titel ist erforderlich.")
    return event_repo.create_event(db, data)

def update_event(db: Session, event_id: int, form: dict) -> Event:
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        raise AdminEventError("Event nicht gefunden.")

    data = {
        "title": form["title"].strip(),
        "description": (form.get("description") or "").strip() or None,
        "location": (form.get("location") or "").strip() or None,
        "starts_at": _parse_datetime_local(form.get("starts_at")),
        "ends_at": _parse_datetime_local(form.get("ends_at")),
        "max_participants": int(form.get("max_participants") or 0),
        "is_active": True if form.get("is_active") == "1" else False,
    }
    if not data["title"]:
        raise AdminEventError("Titel ist erforderlich.")
    return event_repo.update_event(db, event, data)
