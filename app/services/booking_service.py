from datetime import datetime
from sqlalchemy.orm import Session
from ..repositories import event_repo, booking_repo

class BookingError(Exception):
    pass

def book_event(db: Session, user_id: int, event_id: int) -> None:
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        raise BookingError("Event nicht gefunden.")

    if not event.is_active:
        raise BookingError("Dieses Event ist nicht aktiv.")

    # optional: vergangene Events nicht buchbar
    if event.starts_at and event.starts_at < datetime.utcnow():
        raise BookingError("Dieses Event liegt in der Vergangenheit.")

    if booking_repo.exists_booking(db, user_id=user_id, event_id=event_id):
        raise BookingError("Du bist bereits für dieses Event angemeldet.")

    if event.max_participants and event.max_participants > 0:
        current = booking_repo.count_booked_for_event(db, event_id=event_id)
        if current >= event.max_participants:
            raise BookingError("Dieses Event ist bereits ausgebucht.")

    booking_repo.create_booking(db, user_id=user_id, event_id=event_id)
