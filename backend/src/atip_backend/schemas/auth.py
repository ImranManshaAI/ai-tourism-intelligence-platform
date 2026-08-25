from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """Request schema for user authentication."""

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class RefreshTokenRequest(BaseModel):
    """Request schema for refreshing an access token."""

    refresh_token: str = Field(
        min_length=1,
    )


class TokenResponse(BaseModel):
    """Response schema containing authentication tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public representation of an authenticated user."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    email: EmailStr
    role: str
    is_active: bool