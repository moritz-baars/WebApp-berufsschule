from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ...config import templates

router = APIRouter()

@router.get("/confirm", response_class=HTMLResponse)
def booking_confirm(request: Request):
    return templates.TemplateResponse("booking_confirm.html", {"request": request})
