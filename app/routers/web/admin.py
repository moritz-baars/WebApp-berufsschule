from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ...deps import get_db
from fastapi.templating import Jinja2Templates

from ...config import templates

router = APIRouter()

@router.get("/events", response_class=HTMLResponse)
def admin_events(request: Request, db: Session = Depends(get_db)):
    # später: Admin sieht alle Events + Buttons
    return templates.TemplateResponse("admin_events.html", {"request": request})

@router.get("/events/{event_id}/attendees", response_class=HTMLResponse)
def admin_attendees(event_id: int, request: Request, db: Session = Depends(get_db)):
    # später: BookingRepo -> Teilnehmerliste
    return templates.TemplateResponse("admin_attendees.html", {"request": request, "event_id": event_id})
