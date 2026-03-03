from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import socketio
from datetime import datetime

# ----------------- App -----------------
app = FastAPI()

# ----------------- CORS (MANDATORY) -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Socket.IO -----------------
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

socket_app = socketio.ASGIApp(sio, app)

# ----------------- Health Check -----------------
@app.get("/")
async def root():
    return {"status": "FindMe cloud server running"}

# ----------------- Favicon (optional) -----------------
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")

# ----------------- Report Endpoint (MATCH FRONTEND) -----------------
@app.post("/report")
async def submit_report(data: dict):
    alert = {
        "event": "NEW_REPORT",
        "description": data.get("description"),
        "location": data.get("locationName"),
        "time": str(datetime.now())
    }

    # Emit to dashboard
    await sio.emit("alert", alert)

    return {"message": "Report received. Pending verification."}

# ----------------- Socket Events -----------------
@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)