from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ...deps import get_db, get_current_user_optional
from ...services import event_service
from ...config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    q: Optional[str] = None,
    active: int = 1,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_optional),
):
    events, free_map = event_service.get_events_for_homepage(db=db, q=q, active=active)
    return templates.TemplateResponse(
    "home.html",
    {
        "request": request,
        "events": events,
        "free_map": free_map,
        "q": q or "",
        "active": active,
        "user": user
    }
)
