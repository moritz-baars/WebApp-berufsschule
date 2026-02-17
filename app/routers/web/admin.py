from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ...deps import get_db, require_admin
from ...config import templates
from ...services import admin_event_service

router = APIRouter()

@router.get("/events", response_class=HTMLResponse)
def admin_events(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(require_admin),
):
    events = admin_event_service.list_events(db)
    return templates.TemplateResponse(
        "admin_events.html",
        {"request": request, "events": events, "user": user},
    )

@router.get("/events/new", response_class=HTMLResponse)
def admin_new_event_form(
    request: Request,
    user = Depends(require_admin),
):
    return templates.TemplateResponse(
        "admin_event_form.html",
        {"request": request, "user": user, "mode": "create", "event": None, "error": None},
    )

@router.post("/events/new")
def admin_create_event(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    location: str = Form(""),
    starts_at: str = Form(""),
    ends_at: str = Form(""),
    max_participants: str = Form("0"),
    is_active: str = Form("0"),
    db: Session = Depends(get_db),
    user = Depends(require_admin),
):
    try:
        e = admin_event_service.create_event(db, {
            "title": title,
            "description": description,
            "location": location,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "max_participants": max_participants,
            "is_active": is_active,
        })
        return RedirectResponse(url=f"/admin/events/{e.id}", status_code=303)
    except admin_event_service.AdminEventError as ex:
        return templates.TemplateResponse(
            "admin_event_form.html",
            {"request": request, "user": user, "mode": "create", "event": None, "error": str(ex)},
        )

@router.get("/events/{event_id}", response_class=HTMLResponse)
def admin_event_detail(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(require_admin),
):
    try:
        event, attendees = admin_event_service.get_event_detail(db, event_id)
        return templates.TemplateResponse(
            "admin_event_detail.html",
            {"request": request, "user": user, "event": event, "attendees": attendees},
        )
    except admin_event_service.AdminEventError:
        return HTMLResponse("Event nicht gefunden", status_code=404)

@router.get("/events/{event_id}/edit", response_class=HTMLResponse)
def admin_edit_event_form(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(require_admin),
):
    try:
        event, _ = admin_event_service.get_event_detail(db, event_id)
        return templates.TemplateResponse(
            "admin_event_form.html",
            {"request": request, "user": user, "mode": "edit", "event": event, "error": None},
        )
    except admin_event_service.AdminEventError:
        return HTMLResponse("Event nicht gefunden", status_code=404)

@router.post("/events/{event_id}/edit")
def admin_update_event(
    event_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    location: str = Form(""),
    starts_at: str = Form(""),
    ends_at: str = Form(""),
    max_participants: str = Form("0"),
    is_active: str = Form("0"),
    db: Session = Depends(get_db),
    user = Depends(require_admin),
):
    try:
        admin_event_service.update_event(db, event_id, {
            "title": title,
            "description": description,
            "location": location,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "max_participants": max_participants,
            "is_active": is_active,
        })
        return RedirectResponse(url=f"/admin/events/{event_id}", status_code=303)
    except admin_event_service.AdminEventError as ex:
        # event fürs Re-Render holen
        event, _ = admin_event_service.get_event_detail(db, event_id)
        return templates.TemplateResponse(
            "admin_event_form.html",
            {"request": request, "user": user, "mode": "edit", "event": event, "error": str(ex)},
        )
