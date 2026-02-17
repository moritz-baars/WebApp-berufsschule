from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, Dict, List
from datetime import datetime
from ..models import Booking

def exists_booking(db: Session, user_id: int, event_id: int) -> bool:
    return db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.event_id == event_id,
        Booking.status == "booked",
    ).first() is not None

def count_booked_for_event(db: Session, event_id: int) -> int:
    return db.query(func.count(Booking.id)).filter(
        Booking.event_id == event_id,
        Booking.status == "booked",
    ).scalar() or 0

def create_booking(db: Session, user_id: int, event_id: int) -> Booking:
    b = Booking(user_id=user_id, event_id=event_id, status="booked")
    db.add(b)
    db.commit()
    db.refresh(b)
    return b

def count_bookings_grouped_by_event(db: Session) -> Dict[int, int]:
    rows = (
        db.query(Booking.event_id, func.count(Booking.id))
        .filter(Booking.status == "booked")
        .group_by(Booking.event_id)
        .all()
    )
    return {event_id: count for event_id, count in rows}

def list_bookings_for_user(db: Session, user_id: int) -> List[Booking]:
    return (
        db.query(Booking)
        .options(joinedload(Booking.event))
        .filter(
            Booking.user_id == user_id,
            Booking.status.in_(["booked", "cancelled"])
        )
        .order_by(Booking.id.desc())
        .all()
    )

def get_booking_for_user(
    db: Session,
    booking_id: int,
    user_id: int
) -> Optional[Booking]:
    return db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()

def cancel_booking(db: Session, booking: Booking) -> None:
    booking.status = "cancelled"
    db.commit()

def get_booking_any_status(db: Session, user_id: int, event_id: int) -> Optional[Booking]:
    return db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.event_id == event_id
    ).first()

def reactivate_booking(db: Session, booking: Booking) -> Booking:
    booking.status = "booked"
    booking.booked_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking

def list_attendees_for_event(db: Session, event_id: int) -> List[Booking]:
    return (
        db.query(Booking)
        .options(joinedload(Booking.user))
        .filter(
            Booking.event_id == event_id,
            Booking.status == "booked"
        )
        .order_by(Booking.booked_at.desc())
        .all()
    )