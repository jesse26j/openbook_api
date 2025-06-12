from fastapi import FastAPI
from app.api import auth, service, availability, booking





app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(service.router, tags=["services"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(service.router, tags=["services"])
app.include_router(availability.router, tags=["availability"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(service.router, tags=["services"])
app.include_router(availability.router, tags=["availability"])
app.include_router(booking.router, tags=["bookings"])
