from datetime import datetime, timedelta
from typing import List, Set, Tuple

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Event, User, Booking

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed():
    db: Session = SessionLocal()

    now = datetime.utcnow()

    # =========================
    # RESET (reproduzierbar)
    # Reihenfolge: child -> parent
    # =========================
    db.query(Booking).delete()
    db.query(Event).delete()
    db.query(User).delete()
    db.commit()

    # =========================
    # USERS
    # =========================
    admin = User(
        name="Max Mustermann",
        email="admin@firma-initial.de",
        password_hash=hash_password("Admin123!"),
        role="admin",
    )

    employees: List[User] = [
        User(
            name="Anna Becker",
            email="anna.becker@firma-initial.de",
            password_hash=hash_password("Test123!"),
            role="user",
        ),
        User(
            name="Lukas Schmidt",
            email="lukas.schmidt@firma-initial.de",
            password_hash=hash_password("Test123!"),
            role="user",
        ),
        User(
            name="Fatima Kaya",
            email="fatima.kaya@firma-initial.de",
            password_hash=hash_password("Test123!"),
            role="user",
        ),
        User(
            name="Jonas Weber",
            email="jonas.weber@firma-initial.de",
            password_hash=hash_password("Test123!"),
            role="user",
        ),
        User(
            name="Sophie Neumann",
            email="sophie.neumann@firma-initial.de",
            password_hash=hash_password("Test123!"),
            role="user",
        ),
        User(
            name="Mehmet Yilmaz",
            email="mehmet.yilmaz@firma-initial.de",
            password_hash=hash_password("Test123!"),
            role="user",
        ),
    ]

    db.add(admin)
    db.add_all(employees)
    db.commit()

    # (IDs sind jetzt da)
    db.refresh(admin)
    for u in employees:
        db.refresh(u)

    # =========================
    # EVENTS – VERGANGEN (Fortbildungen)
    # =========================
    past_events: List[Event] = [
        Event(
            title="IT-Sicherheit Grundlagen",
            description="Passwortsicherheit, Phishing-Erkennung und sichere Arbeitsweise.",
            starts_at=now - timedelta(days=60),
            location="Raum A1",
            max_participants=20,
            is_active=False,
        ),
        Event(
            title="DSGVO & Datenschutz",
            description="Rechtliche Grundlagen und praktische Umsetzung im Arbeitsalltag.",
            starts_at=now - timedelta(days=30),
            location="Seminarraum 2",
            max_participants=25,
            is_active=False,
        ),
        Event(
            title="Kommunikation im Team",
            description="Effektive Kommunikation und Konfliktlösung im Unternehmen.",
            starts_at=now - timedelta(days=15),
            location="Konferenzraum 1",
            max_participants=15,
            is_active=False,
        ),
    ]

    # =========================
    # EVENTS – ZUKÜNFTIG (Fortbildungen)
    # =========================
    future_events: List[Event] = [
        Event(
            title="Fortbildung: KI im Unternehmen",
            description="Praktische Anwendungen von KI-Tools zur Effizienzsteigerung.",
            starts_at=now + timedelta(days=7),
            location="Seminarraum 3",
            max_participants=30,
            is_active=True,
        ),
        Event(
            title="Excel Advanced Workshop",
            description="Pivot-Tabellen, Makros und Datenanalyse für Fortgeschrittene.",
            starts_at=now + timedelta(days=14),
            location="Raum B1",
            max_participants=6,  # bewusst klein, damit man 'voll' testen kann
            is_active=True,
        ),
        Event(
            title="Agiles Projektmanagement (Scrum)",
            description="Einführung in Scrum und agile Methoden.",
            starts_at=now + timedelta(days=21),
            location="Konferenzraum 2",
            max_participants=12,
            is_active=True,
        ),
        Event(
            title="Zeitmanagement & Selbstorganisation",
            description="Effiziente Arbeitsmethoden für den Büroalltag.",
            starts_at=now + timedelta(days=28),
            location="Online (MS Teams)",
            max_participants=50,
            is_active=True,
        ),
        Event(
            title="Erste Hilfe im Betrieb",
            description="Grundlagen der Ersten Hilfe für Mitarbeiter.",
            starts_at=now + timedelta(days=35),
            location="Raum A2",
            max_participants=12,
            is_active=True,
        ),
    ]

    db.add_all(past_events + future_events)
    db.commit()

    # Events refreshen (IDs)
    all_events: List[Event] = db.query(Event).all()
    past_events_db = [e for e in all_events if e.starts_at and e.starts_at < now]
    future_events_db = [e for e in all_events if e.starts_at and e.starts_at > now]

    # =========================
    # BOOKINGS (ohne Duplikate)
    # Unique constraint: (user_id, event_id)
    # =========================
    created_pairs: Set[Tuple[int, int]] = set()
    bookings: List[Booking] = []

    def add_booking(user_id: int, event_id: int, status: str = "booked"):
        key = (user_id, event_id)
        if key in created_pairs:
            return
        created_pairs.add(key)
        bookings.append(Booking(user_id=user_id, event_id=event_id, status=status))

    # 1) Vergangene Events: einige Mitarbeiter waren dabei (nicht alle)
    for ev in past_events_db:
        for u in employees[:4]:  # nur 4 von 6
            add_booking(u.id, ev.id, status="booked")

    # 2) Erstes zukünftiges Event: teilweise gebucht
    if future_events_db:
        ev = future_events_db[0]
        add_booking(employees[0].id, ev.id)
        add_booking(employees[1].id, ev.id)
        add_booking(employees[2].id, ev.id)

    # 3) Zweites zukünftiges Event: voll (genau max_participants)
    if len(future_events_db) > 1:
        ev = future_events_db[1]
        slots = ev.max_participants or len(employees)
        # fülle mit unterschiedlichen Mitarbeitern bis slots erreicht
        for i in range(slots):
            u = employees[i % len(employees)]
            add_booking(u.id, ev.id)

    # 4) Letztes zukünftiges Event: eine stornierte Buchung
    if future_events_db:
        ev = future_events_db[-1]
        add_booking(employees[0].id, ev.id, status="canceled")

    db.add_all(bookings)
    db.commit()

    db.close()
    print("Seed erfolgreich abgeschlossen.")
    print("Admin Login: admin@firma-initial.de / Admin123!")
    print("User Login:  anna.becker@firma-initial.de / Test123!")


if __name__ == "__main__":
    seed()
