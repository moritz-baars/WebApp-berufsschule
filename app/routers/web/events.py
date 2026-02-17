from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models import Event
from ...config import templates
from fastapi.templating import Jinja2Templates

router = APIRouter()

@router.get("/{event_id}", response_class=HTMLResponse)
def event_detail(event_id: int, request: Request, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        # später: 404 Seite
        return HTMLResponse("Event nicht gefunden", status_code=404)
    return templates.TemplateResponse("event_detail.html", {"request": request, "event": event})

@router.post("/{event_id}/book")
def book_event(event_id: int, db: Session = Depends(get_db)):
    # später: BookingService.book_event(user_id, event_id)
    # erstmal nur redirect als Platzhalter
    return RedirectResponse(url=f"/events/{event_id}", status_code=303)
