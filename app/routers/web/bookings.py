from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ...deps import get_db, get_current_user_optional, get_current_user
from ...repositories import event_repo, booking_repo
from ...services import booking_service
from ...config import templates


router = APIRouter()

@router.get("/confirm", response_class=HTMLResponse)
def booking_success(
    request: Request,
    event_id: int | None = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_optional),
):
    event = event_repo.get_event_by_id(db, event_id) if event_id else None

    return templates.TemplateResponse(
        "booking_success.html",
        {"request": request, "user": user, "event": event},
    )

@router.get("/mine", response_class=HTMLResponse)
def my_bookings(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    bookings = booking_service.get_user_bookings(db, user.id)

    return templates.TemplateResponse(
        "my_bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "user": user
        }
    )


@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    try:
        booking_service.cancel_user_booking(db, user.id, booking_id)
    except Exception:
        pass

    return RedirectResponse(url="/bookings/mine", status_code=303)
