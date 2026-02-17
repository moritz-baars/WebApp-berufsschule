from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict
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