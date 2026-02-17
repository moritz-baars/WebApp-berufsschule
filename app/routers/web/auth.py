from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ...deps import get_db
from ...services import auth_service
from ...config import templates

router = APIRouter()

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # 1 Basic Validation
    if not name.strip() or not email.strip() or not password.strip():
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Alle Felder müssen ausgefüllt werden.",
                "name": name,
                "email": email
            }
        )

    try:
        user = auth_service.register_user(db, name.strip(), email.strip().lower(), password)
        request.session["user_id"] = user.id

        return RedirectResponse(url="/", status_code=303)

    except ValueError:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Email ist bereits registriert.",
                "name": name,
                "email": email
            }
        )

    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Registrierung fehlgeschlagen.",
                "name": name,
                "email": email
            }
        )


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Basic Validation
    if not email.strip() or not password.strip():
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Bitte Email und Passwort eingeben.",
                "email": email
            }
        )

    # Email normalisieren
    email = email.strip().lower()

    # Authentifizieren
    user = auth_service.authenticate_user(db, email, password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Falsche Zugangsdaten.",
                "email": email
            }
        )

    # Session setzen (alte Session sicherheitshalber löschen)
    request.session.clear()
    request.session["user_id"] = user.id
    request.session["role"] = user.role 

    return RedirectResponse(url="/", status_code=303)



@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)



