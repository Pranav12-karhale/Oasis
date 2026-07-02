"""
Oasis Auth Service — JWT Authentication + Google OAuth
"""

import os
import uuid
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
import redis.asyncio as redis


# ── Config ───────────────────────────────────────────────────────────────────
JWT_SECRET = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

logger = logging.getLogger("oasis.auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

app = FastAPI(title="Oasis Auth Service", version="0.1.0")


# ── Models ───────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    """Registration request."""
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=2, max_length=100)
    preferred_language: str = Field(default="en")


class UserLogin(BaseModel):
    """Login request."""
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    """Full user profile."""
    id: str
    email: str
    name: str
    preferred_language: str = "en"
    accessibility_mode: str = "standard"  # standard | voice | isl | simplified
    saved_locations: list[dict] = []
    health_conditions: list[str] = []  # For personalized advisories
    notification_prefs: dict = Field(default_factory=lambda: {
        "push": True, "whatsapp": False, "sms": False, "email": True
    })
    narration_speed: float = 1.0  # 0.5–2.0 for TTS
    created_at: str = ""


class TokenResponse(BaseModel):
    """JWT token pair."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserProfile


class GoogleOAuthRequest(BaseModel):
    """Google OAuth token exchange."""
    id_token: str


class ProfileUpdate(BaseModel):
    """Profile update request."""
    name: Optional[str] = None
    preferred_language: Optional[str] = None
    accessibility_mode: Optional[str] = None
    saved_locations: Optional[list[dict]] = None
    health_conditions: Optional[list[str]] = None
    notification_prefs: Optional[dict] = None
    narration_speed: Optional[float] = None


# ── In-Memory User Store (Replace with PostgreSQL in production) ─────────────
# TODO: Phase 2 — Replace with SQLAlchemy + PostgreSQL
users_db: dict[str, dict] = {}


# ── JWT Helpers ──────────────────────────────────────────────────────────────

def create_access_token(user_id: str) -> str:
    """Create a short-lived access token."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    return jwt.encode(
        {"sub": user_id, "exp": expire, "type": "access"},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def create_refresh_token(user_id: str) -> str:
    """Create a long-lived refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE)
    return jwt.encode(
        {"sub": user_id, "exp": expire, "type": "refresh"},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserProfile:
    """Dependency: extract current user from JWT."""
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**users_db[user_id])


# ═════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "auth"}


@app.post("/register", response_model=TokenResponse)
async def register(req: UserRegister):
    """Register a new user account."""
    # Check if email already exists
    for user in users_db.values():
        if user["email"] == req.email:
            raise HTTPException(status_code=409, detail="Email already registered")

    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "email": req.email,
        "name": req.name,
        "password_hash": pwd_context.hash(req.password),
        "preferred_language": req.preferred_language,
        "accessibility_mode": "standard",
        "saved_locations": [],
        "health_conditions": [],
        "notification_prefs": {"push": True, "whatsapp": False, "sms": False, "email": True},
        "narration_speed": 1.0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    users_db[user_id] = user_data
    logger.info(f"New user registered: {req.email}")

    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
        user=UserProfile(**{k: v for k, v in user_data.items() if k != "password_hash"}),
    )


@app.post("/login", response_model=TokenResponse)
async def login(req: UserLogin):
    """Login with email + password."""
    # Find user by email
    user_data = None
    for user in users_db.values():
        if user["email"] == req.email:
            user_data = user
            break

    if not user_data or not pwd_context.verify(req.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return TokenResponse(
        access_token=create_access_token(user_data["id"]),
        refresh_token=create_refresh_token(user_data["id"]),
        user=UserProfile(**{k: v for k, v in user_data.items() if k != "password_hash"}),
    )


@app.post("/google")
async def google_oauth(req: GoogleOAuthRequest):
    """Login/register via Google OAuth."""
    # TODO: Verify Google ID token with google-auth library
    # For now, return a placeholder
    raise HTTPException(status_code=501, detail="Google OAuth — coming in Phase 2")


@app.get("/profile", response_model=UserProfile)
async def get_profile(user: UserProfile = Depends(get_current_user)):
    """Get current user's profile."""
    return user


@app.put("/profile", response_model=UserProfile)
async def update_profile(
    update: ProfileUpdate,
    user: UserProfile = Depends(get_current_user),
):
    """Update user profile (language, accessibility, health conditions, etc.)."""
    user_data = users_db[user.id]
    update_dict = update.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        user_data[key] = value

    users_db[user.id] = user_data
    logger.info(f"Profile updated for user: {user.id}")
    return UserProfile(**{k: v for k, v in user_data.items() if k != "password_hash"})


@app.delete("/account")
async def delete_account(user: UserProfile = Depends(get_current_user)):
    """Delete user account and all data (DPDPA compliance)."""
    del users_db[user.id]
    logger.info(f"Account deleted (DPDPA request): {user.id}")
    return {"message": "Account and all data deleted successfully"}


# ═════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
