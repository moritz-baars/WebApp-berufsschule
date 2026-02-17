# Barrierefreie Event- und Kursverwaltungs-WebApp

## Projektbeschreibung

Entwicklung einer barrierefreien Web-Applikation zur Verwaltung und Buchung von Events und Kursen.

Die Anwendung ermöglicht:
- Anzeige von Events
- Anmeldung und Abmeldung
- Administrationsoberfläche zur Pflege von Veranstaltungen
- Umsetzung grundlegender WCAG-Richtlinien (Barrierefreiheit)
- Ressourcenschonende Umsetzung im Sinne von Green IT

---

## Technologie-Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy (ORM)
- Jinja2 (Templates)
- Passlib (bcrypt) für Passwort-Hashing
- Uvicorn (ASGI Server)

---

## Projektstruktur

WEBAPP-BERUFSSCHULE/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── deps.py
│   ├── security.py
│   └── routers/
│       ├── __init__.py
│       ├── events.py
│       ├── auth.py
│       └── admin.py
│
├── templates/
├── static/
├── tests/
├── docs/
├── requirements.txt
├── app.db
└── README.md

---

## Virtuelle Umgebung einrichten

### 1) Virtuelle Umgebung erstellen
python -m venv venv

### 2) Aktivieren (Windows)
venv\Scripts\activate

Im Terminal sollte nun stehen:
(venv)

---

## Dependencies installieren

Falls requirements.txt vorhanden:
pip install -r requirements.txt

Falls noch nicht vorhanden:
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] jinja2
pip freeze > requirements.txt

---

## Server starten

Vom Projekt-Root aus:
uvicorn app.main:app --reload

Server erreichbar unter:
http://127.0.0.1:8000

Event-Übersicht:
http://127.0.0.1:8000/events

---

## Datenbank

- SQLite wird als Datei app.db im Projekt-Root erstellt
- Tabellen werden beim Start automatisch erzeugt
- Passwörter werden mit bcrypt gehasht gespeichert
- Unique-Constraint verhindert doppelte Buchungen eines Events

---

## Wichtige Hinweise

- Vor jeder Arbeit virtuelle Umgebung aktivieren
- requirements.txt aktuell halten
- Änderungen am Datenmodell erfordern ggf. Löschen von app.db
- Später kann Alembic für Migrationen genutzt werden

---

## Entwicklungsstand

- Datenbankanbindung mit SQLAlchemy
- User-, Event- und Booking-Modelle
- Test-Create und Test-List Routes
- HTML-Rendering mit Jinja2 vorbereitet
- Virtuelle Umgebung eingerichtet
