from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from ...deps import get_db, get_current_user, get_current_user_optional
from ...services.booking_service import book_event, BookingError
from ...repositories import event_repo
from ...config import templates

router = APIRouter()


@router.get("/{event_id}", response_class=HTMLResponse)
def event_detail(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_optional),
):
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        return HTMLResponse("Event nicht gefunden", status_code=404)

    return templates.TemplateResponse(
        "event_detail.html",
        {
            "request": request,
            "event": event,
            "user": user
        }
    )


@router.get("/{event_id}/book/confirm", response_class=HTMLResponse)
def booking_confirm(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        return HTMLResponse("Event nicht gefunden", status_code=404)

    # simple Schutz: nur wenn Confirm aufgerufen wurde, erlauben wir POST danach
    request.session["pending_booking_event_id"] = event_id

    return templates.TemplateResponse(
        "booking_confirm.html",
        {"request": request, "event": event, "user": user},
    )


@router.post("/{event_id}/book")
def booking_submit(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    pending = request.session.get("pending_booking_event_id")
    if pending != event_id:
        # wurde nicht über Confirm gestartet
        return RedirectResponse(url=f"/events/{event_id}/book/confirm", status_code=303)

    # pending nach Gebrauch löschen (gegen doppelt senden)
    request.session.pop("pending_booking_event_id", None)

    try:
        book_event(db, user_id=user.id, event_id=event_id)
        return RedirectResponse(url=f"/bookings/confirm?event_id={event_id}", status_code=303)
    except BookingError as e:
        # zurück zur Detailseite mit Fehler
        event = event_repo.get_event_by_id(db, event_id)
        return templates.TemplateResponse(
            "event_detail.html",
            {"request": request, "event": event, "user": user, "error": str(e)},
        )
