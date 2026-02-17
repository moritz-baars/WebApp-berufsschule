from datetime import datetime
from sqlalchemy.orm import Session

from ..repositories import event_repo, booking_repo


class BookingError(Exception):
    pass


class BookingCancelError(Exception):
    pass


def book_event(db: Session, user_id: int, event_id: int) -> None:
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        raise BookingError("Event nicht gefunden.")

    if not event.is_active:
        raise BookingError("Dieses Event ist nicht aktiv.")

    # vergangene Events nicht buchbar
    if event.starts_at and event.starts_at < datetime.utcnow():
        raise BookingError("Dieses Event liegt in der Vergangenheit.")

    # Prüfen: gibt es schon eine Buchung (egal welcher Status)?
    existing = booking_repo.get_booking_any_status(db, user_id=user_id, event_id=event_id)

    # Wenn bereits aktiv gebucht -> blocken
    if existing and existing.status == "booked":
        raise BookingError("Du bist bereits für dieses Event angemeldet.")

    # Kapazität prüfen (gilt sowohl für neue Buchung als auch Reaktivierung)
    if event.max_participants and event.max_participants > 0:
        current = booking_repo.count_booked_for_event(db, event_id=event_id)
        if current >= event.max_participants:
            raise BookingError("Dieses Event ist bereits ausgebucht.")

    # Wenn storniert vorhanden -> reaktivieren statt neu erstellen
    if existing and existing.status == "cancelled":
        booking_repo.reactivate_booking(db, existing)
        return

    # Sonst neu erstellen
    booking_repo.create_booking(db, user_id=user_id, event_id=event_id)


def get_user_bookings(db: Session, user_id: int):
    return booking_repo.list_bookings_for_user(db, user_id)


def cancel_user_booking(db: Session, user_id: int, booking_id: int):
    booking = booking_repo.get_booking_for_user(db, booking_id, user_id)

    if not booking:
        raise BookingCancelError("Buchung nicht gefunden.")

    if booking.status == "cancelled":
        raise BookingCancelError("Diese Buchung wurde bereits storniert.")

    booking_repo.cancel_booking(db, booking)
