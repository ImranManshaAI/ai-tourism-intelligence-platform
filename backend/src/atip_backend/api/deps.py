from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from atip_backend.core.security import decode_token
from atip_backend.db.session import SessionLocal
from atip_backend.models.user import User
from atip_backend.services.auth_service import AuthenticationService


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_db():
    """Provide a database session for each request."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    """Return the authenticated user from a valid access token."""

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    try:
        payload = decode_token(
            credentials.credentials,
            expected_token_type="access",
        )

        user_id = UUID(
            payload["sub"]
        )

    except (
        InvalidTokenError,
        ValueError,
        KeyError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    service = AuthenticationService(db)

    user = service.get_user_by_id(
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user