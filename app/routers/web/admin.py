from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ...deps import get_db, require_admin
from ...services import event_service
from fastapi.templating import Jinja2Templates


from ...config import templates

router = APIRouter()

@router.get("/events", response_class=HTMLResponse)
def admin_events(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(require_admin),
):
    events = event_service.get_all_events_for_admin(db)

    return templates.TemplateResponse(
        "admin_events.html",
        {"request": request, "events": events, "user": user},
    )
