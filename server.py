from fastapi import FastAPI
import socketio
from datetime import datetime

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)

@app.post("/submit-report")
async def submit_report(data: dict):
    alert = {
        "event": "NEW_REPORT",
        "name": data.get("name"),
        "location": data.get("location"),
        "time": str(datetime.now())
    }

    await sio.emit("alert", alert)
    return {"status": "ok"}

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)