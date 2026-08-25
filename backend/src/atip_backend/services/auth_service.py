from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from atip_backend.core.config import get_settings
from atip_backend.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from atip_backend.models.auth_session import AuthSession
from atip_backend.models.user import User


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class AuthenticationService:
    """Service responsible for user authentication and sessions."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """Return a user by email."""

        statement = select(User).where(
            User.email == email.strip().lower()
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """Return a user by ID."""

        return self.db.get(
            User,
            user_id,
        )

    def get_session_by_id(
        self,
        session_id: UUID,
    ) -> AuthSession | None:
        """Return an authentication session by ID."""

        return self.db.get(
            AuthSession,
            session_id,
        )

    def validate_refresh_session(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
        refresh_token: str,
    ) -> AuthSession:
        """Validate a refresh token against its database session."""

        auth_session = self.get_session_by_id(
            session_id
        )

        if auth_session is None:
            raise AuthenticationError(
                "Invalid refresh session"
            )

        if auth_session.user_id != user_id:
            raise AuthenticationError(
                "Invalid refresh session"
            )

        if auth_session.revoked_at is not None:
            raise AuthenticationError(
                "Refresh session has been revoked"
            )

        now = datetime.now(
            timezone.utc
        )

        expires_at = auth_session.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(
                tzinfo=timezone.utc
            )

        if expires_at <= now:
            raise AuthenticationError(
                "Refresh session has expired"
            )

        if not verify_password(
            refresh_token,
            auth_session.refresh_token_hash,
        ):
            raise AuthenticationError(
                "Invalid refresh token"
            )

        return auth_session

    def authenticate(
        self,
        *,
        email: str,
        password: str,
    ) -> User:
        """Authenticate a user with email and password."""

        user = self.get_user_by_email(email)

        if user is None:
            raise AuthenticationError(
                "Invalid credentials"
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise AuthenticationError(
                "Invalid credentials"
            )

        if not user.is_active:
            raise AuthenticationError(
                "User account is inactive"
            )

        return user

    def _create_auth_session(
        self,
        user: User,
    ) -> tuple[str, AuthSession]:
        """Create a refresh token and its database-backed session."""

        settings = get_settings()

        session_id = uuid4()

        refresh_token = create_refresh_token(
            str(user.id),
            session_id=str(session_id),
        )

        expires_at = datetime.now(
            timezone.utc
        ) + timedelta(
            days=settings.refresh_token_expire_days
        )

        auth_session = AuthSession(
            id=session_id,
            user_id=user.id,
            refresh_token_hash=hash_password(
                refresh_token
            ),
            expires_at=expires_at,
        )

        self.db.add(auth_session)

        return refresh_token, auth_session

    def create_token_pair(
        self,
        user: User,
    ) -> tuple[str, str]:
        """Create an access token and database-backed refresh token."""

        refresh_token, _ = self._create_auth_session(
            user
        )

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        access_token = create_access_token(
            str(user.id)
        )

        return access_token, refresh_token

    def revoke_session(
        self,
        auth_session: AuthSession,
    ) -> None:
        """Revoke an authentication session."""

        auth_session.revoked_at = datetime.now(
            timezone.utc
        )

    def rotate_refresh_token(
        self,
        *,
        user: User,
        current_session: AuthSession,
    ) -> tuple[str, str]:
        """
        Revoke the current refresh session and create
        a new access/refresh token pair.
        """

        self.revoke_session(
            current_session
        )

        refresh_token, _ = self._create_auth_session(
            user
        )

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        access_token = create_access_token(
            str(user.id)
        )

        return access_token, refresh_token