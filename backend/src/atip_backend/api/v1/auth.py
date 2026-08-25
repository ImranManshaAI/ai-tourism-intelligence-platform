from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from atip_backend.api.deps import get_current_user, get_db
from atip_backend.core.security import decode_token
from atip_backend.models.user import User
from atip_backend.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse,
)
from atip_backend.services.auth_service import (
    AuthenticationError,
    AuthenticationService,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate a user and return an access/refresh token pair."""

    service = AuthenticationService(db)

    try:
        user = service.authenticate(
            email=str(credentials.email),
            password=credentials.password,
        )

        access_token, refresh_token = (
            service.create_token_pair(user)
        )

    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Validate a refresh token and rotate it.

    The previous refresh session is revoked and a new
    access/refresh token pair is created.
    """

    try:
        payload = decode_token(
            request.refresh_token,
            expected_token_type="refresh",
        )

        user_id = UUID(
            payload["sub"]
        )

        session_id = UUID(
            payload["sid"]
        )

    except (
        InvalidTokenError,
        ValueError,
        KeyError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    service = AuthenticationService(db)

    user = service.get_user_by_id(
        user_id
    )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    try:
        current_session = service.validate_refresh_session(
            session_id=session_id,
            user_id=user.id,
            refresh_token=request.refresh_token,
        )

        access_token, refresh_token = (
            service.rotate_refresh_token(
                user=user,
                current_session=current_session,
            )
        )

    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    """Return the currently authenticated user."""

    return current_user