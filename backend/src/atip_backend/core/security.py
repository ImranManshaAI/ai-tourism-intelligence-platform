from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from atip_backend.core.config import get_settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2."""

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a plaintext password against its stored hash."""

    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed JWT with standard application claims."""

    settings = get_settings()

    now = datetime.now(timezone.utc)
    expires_at = now + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": now,
        "exp": expires_at,
        "jti": str(uuid4()),
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(
    subject: str,
) -> str:
    """Create a short-lived access token."""

    settings = get_settings()

    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes
        ),
    )


def create_refresh_token(
    subject: str,
    *,
    session_id: str,
) -> str:
    """Create a longer-lived refresh token bound to a session."""

    settings = get_settings()

    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(
            days=settings.refresh_token_expire_days
        ),
        extra_claims={
            "sid": session_id,
        },
    )


def decode_token(
    token: str,
    *,
    expected_token_type: str,
) -> dict[str, Any]:
    """Decode and validate a JWT."""

    settings = get_settings()

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )

    token_type = payload.get("type")

    if token_type != expected_token_type:
        raise InvalidTokenError(
            "Invalid token type"
        )

    subject = payload.get("sub")

    if not subject:
        raise InvalidTokenError(
            "Token subject is missing"
        )

    if expected_token_type == "refresh" and not payload.get("sid"):
        raise InvalidTokenError(
            "Refresh token session ID is missing"
        )

    return payload
