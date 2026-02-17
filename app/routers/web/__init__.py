from fastapi import APIRouter
from . import pages, events, bookings, admin, auth

web_router = APIRouter()

web_router.include_router(pages.router)
web_router.include_router(events.router, prefix="/events", tags=["web-events"])
web_router.include_router(bookings.router, prefix="/bookings", tags=["web-bookings"])
web_router.include_router(auth.router, prefix="/auth", tags=["web-auth"])
web_router.include_router(admin.router, prefix="/admin", tags=["web-admin"])
