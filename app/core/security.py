import hashlib, hmac, base64, json, time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
from app.core.config import settings

def get_password_hash(password: str) -> str:
    salt = "pulseops_salt_"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = int((datetime.now(timezone.utc) + expires_delta).timestamp())
    else:
        expire = int((datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    payload = {"sub": str(subject), "exp": expire}
    header = {"alg": "HS256", "typ": "JWT"}
    h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    sig = hmac.new(settings.SECRET_KEY.encode(), f"{ h_b64}.{ p_b64}".replace(" ", "").encode(), hashlib.sha256).digest()
    s_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return h_b64 + "." + p_b64 + "." + s_b64

def decode_access_token(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        h_b64, p_b64, s_b64 = parts
        rem = len(p_b64) % 4
        if rem:
            p_b64 += "=" * (4 - rem)
        payload = json.loads(base64.urlsafe_b64decode(p_b64.encode()).decode())
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload
    except Exception:
        return None
