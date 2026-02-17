from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .db import Base, engine
from . import models  # wichtig: damit SQLAlchemy Models registriert sind

from .routers.web import web_router
from .routers.api import api_router

app = FastAPI()

# Static Files (CSS, Bilder etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sessions
app.add_middleware(
    SessionMiddleware,
    secret_key="1ad56fc62d675fd0121163f0c29f4b8e62447f37e86bbc886456cb2d3d167779",
    same_site="lax"
)

# DB Tabellen erstellen (für den Anfang ok; später Alembic)
Base.metadata.create_all(bind=engine)

# Router registrieren
app.include_router(web_router)
app.include_router(api_router)



