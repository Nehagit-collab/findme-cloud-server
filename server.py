from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from datetime import datetime

# ----------------- Socket.IO -----------------
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

# ----------------- FastAPI App -----------------
app = FastAPI()

# ----------------- CORS (MANDATORY) -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Root Health Check (IMPORTANT) -----------------
@app.get("/")
async def root():
    return {"status": "FindMe cloud server running"}

# ----------------- Report Endpoint (USED BY USER HTML) -----------------
@app.post("/report")
async def submit_report(data: dict):
    """
    Expected payload from user HTML:
    {
        image: base64,
        description: string,
        locationName: string
    }
    """

    alert = {
        "message": f"New sighting reported at {data.get('locationName')}",
        "description": data.get("description"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Emit alert to ALL connected dashboards
    await sio.emit("alert", alert)

    return {
        "message": "Report received. Pending verification."
    }

# ----------------- Socket Events -----------------
@sio.event
async def connect(sid, environ):
    print("✅ Dashboard connected:", sid)

@sio.event
async def disconnect(sid):
    print("❌ Dashboard disconnected:", sid)

# ----------------- ASGI App (IMPORTANT) -----------------
socket_app = socketio.ASGIApp(sio, app)