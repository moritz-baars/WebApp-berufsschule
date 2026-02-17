from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...deps import get_db
from ...models import Event

router = APIRouter()

@router.get("/")
def api_list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return [{"id": e.id, "title": e.title} for e in events]

@router.get("/{event_id}")
def api_get_event(event_id: int, db: Session = Depends(get_db)):
    e = db.query(Event).filter(Event.id == event_id).first()
    if not e:
        return {"error": "not found"}
    return {"id": e.id, "title": e.title, "description": e.description}
