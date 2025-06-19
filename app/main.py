from fastapi import FastAPI, WebSocket
from app.api import auth, service, availability, booking, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend dev server (Vite default)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    # Optionally: validate token
    await websocket.accept()
    await websocket.send_text("WebSocket connected")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(service.router, tags=["services"])
app.include_router(availability.router, tags=["availability"])
app.include_router(booking.router, tags=["bookings"])
app.include_router(users.router, tags=["users"])
