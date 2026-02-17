from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ...deps import get_db, get_current_user_optional
from ...repositories import event_repo
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

