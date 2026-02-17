from fastapi import APIRouter
from . import events, bookings

api_router = APIRouter(prefix="/api")

api_router.include_router(events.router, prefix="/events", tags=["api-events"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["api-bookings"])
