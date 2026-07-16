from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any

from jose import JWTError, jwt

from backend.app.core.config import settings
from backend.app.exceptions.exceptions import AuthenticationError

CLINIC_USERNAME = "admin"
CLINIC_PASSWORD_HASH = sha256("rashid123".encode()).hexdigest()


def verify_password(plain_password: str) -> bool:
    return sha256(plain_password.encode()).hexdigest() == CLINIC_PASSWORD_HASH


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key or "dev-secret-key", algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.secret_key or "dev-secret-key",
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        raise AuthenticationError("Invalid or expired token.")


def authenticate_user(username: str, password: str) -> str:
    if username != CLINIC_USERNAME:
        raise AuthenticationError("Invalid username or password.")
    if not verify_password(password):
        raise AuthenticationError("Invalid username or password.")
    return create_access_token({"sub": username, "role": "admin"})
