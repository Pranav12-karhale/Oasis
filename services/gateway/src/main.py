"""
Oasis API Gateway — FastAPI Application
Single entry point for all client requests. Handles routing, auth, rate limiting.
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import redis.asyncio as redis

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.gateway")


# ── Lifespan (startup/shutdown) ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize shared resources on startup, clean up on shutdown."""
    # Startup
    app.state.redis = redis.from_url(
        f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}",
        decode_responses=True,
    )
    app.state.http_client = httpx.AsyncClient(timeout=30.0)
    logger.info("🏝️  Oasis Gateway started successfully")

    yield

    # Shutdown
    await app.state.http_client.aclose()
    await app.state.redis.aclose()
    logger.info("Oasis Gateway shut down")


# ── App Initialization ──────────────────────────────────────────────────────
app = FastAPI(
    title="Oasis — Health & Safety Advisory Platform",
    description=(
        "AI-powered health and safety recommendations based on real-time climate, "
        "disaster, pollution, and crisis data across India. Accessible to all — "
        "including deaf and blind communities — in 13+ Indian languages."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── OpenTelemetry Instrumentation ────────────────────────────────────────────
FastAPIInstrumentor.instrument_app(app)


# ── Service URLs ─────────────────────────────────────────────────────────────
AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8001")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8002")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "http://notification:8007")


# ═════════════════════════════════════════════════════════════════════════════
# HEALTH & SYSTEM ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.get("/health", tags=["System"])
async def health_check():
    """Kubernetes liveness/readiness probe."""
    return {"status": "healthy", "service": "gateway", "version": "0.1.0"}


@app.get("/api/v1/languages", tags=["System"])
async def get_supported_languages():
    """Return all supported languages."""
    return {
        "languages": [
            {"code": "en", "name": "English", "script": "Latin", "native": "English"},
            {"code": "hi", "name": "Hindi", "script": "Devanagari", "native": "हिन्दी"},
            {"code": "mr", "name": "Marathi", "script": "Devanagari", "native": "मराठी"},
            {"code": "bn", "name": "Bengali", "script": "Bengali", "native": "বাংলা"},
            {"code": "gu", "name": "Gujarati", "script": "Gujarati", "native": "ગુજરાતી"},
            {"code": "ta", "name": "Tamil", "script": "Tamil", "native": "தமிழ்"},
            {"code": "te", "name": "Telugu", "script": "Telugu", "native": "తెలుగు"},
            {"code": "kn", "name": "Kannada", "script": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "ml", "name": "Malayalam", "script": "Malayalam", "native": "മലയാളം"},
            {"code": "pa", "name": "Punjabi", "script": "Gurmukhi", "native": "ਪੰਜਾਬੀ"},
            {"code": "or", "name": "Odia", "script": "Odia", "native": "ଓଡ଼ିଆ"},
            {"code": "as", "name": "Assamese", "script": "Assamese", "native": "অসমীয়া"},
            {"code": "ur", "name": "Urdu", "script": "Perso-Arabic", "native": "اردو"},
        ]
    }


# ═════════════════════════════════════════════════════════════════════════════
# AUTH PROXY ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/auth/register", tags=["Auth"])
async def register(request: Request):
    """Proxy registration to auth service."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/register", json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@app.post("/api/v1/auth/login", tags=["Auth"])
async def login(request: Request):
    """Proxy login to auth service."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/login", json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@app.post("/api/v1/auth/google", tags=["Auth"])
async def google_oauth(request: Request):
    """Proxy Google OAuth to auth service."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/google", json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


# ═════════════════════════════════════════════════════════════════════════════
# CORE QUERY ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/query", tags=["Core"])
async def submit_query(request: Request):
    """
    Submit a natural language health/safety query (text).
    
    Request body:
    {
        "query": "Is it safe to go outside today?",
        "location": {"lat": 19.076, "lng": 72.8777, "city": "Mumbai"},
        "language": "hi",
        "accessibility_mode": "standard"
    }
    """
    body = await request.json()

    # Validate required fields
    if "query" not in body:
        raise HTTPException(status_code=400, detail="'query' field is required")

    # Forward to orchestrator
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{ORCHESTRATOR_URL}/process", json={
            "input_text": body["query"],
            "input_modality": "text",
            "location": body.get("location", {}),
            "language": body.get("language", "en"),
            "accessibility_mode": body.get("accessibility_mode", "standard"),
        })

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Orchestrator service unavailable")

    return resp.json()


@app.post("/api/v1/query/voice", tags=["Core"])
async def submit_voice_query(request: Request):
    """
    Submit a voice-based health/safety query (audio upload).
    Accepts multipart form data with audio file.
    """
    form = await request.form()
    audio_file = form.get("audio")
    language = form.get("language", "auto")
    location = form.get("location", "{}")

    if not audio_file:
        raise HTTPException(status_code=400, detail="Audio file is required")

    # Forward audio to orchestrator with voice modality
    audio_bytes = await audio_file.read()
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{ORCHESTRATOR_URL}/process",
            json={
                "input_modality": "voice",
                "language": language,
                "location": location,
                "accessibility_mode": "voice",
            },
            files={"audio": ("query.webm", audio_bytes, "audio/webm")},
        )

    return resp.json()


@app.get("/api/v1/alerts/{city}", tags=["Alerts"])
async def get_alerts(city: str, state: str = None):
    """Get active weather, disaster, and pollution alerts for a city."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            f"{ORCHESTRATOR_URL}/alerts",
            params={"city": city, "state": state},
        )
    return resp.json()


@app.post("/api/v1/assess", tags=["Core"])
async def health_risk_assessment(request: Request):
    """
    Full health risk assessment for a location.
    Aggregates weather + pollution + disaster + health data.
    """
    body = await request.json()
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{ORCHESTRATOR_URL}/assess", json=body)
    return resp.json()


# ═════════════════════════════════════════════════════════════════════════════
# NOTIFICATION ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/notifications/subscribe", tags=["Notifications"])
async def subscribe_notifications(request: Request):
    """Subscribe to push alerts for a location."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{NOTIFICATION_URL}/subscribe", json=body)
    return resp.json()


@app.delete("/api/v1/notifications/unsubscribe", tags=["Notifications"])
async def unsubscribe_notifications(request: Request):
    """Unsubscribe from push alerts."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{NOTIFICATION_URL}/unsubscribe", json=body)
    return resp.json()


# ═════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
