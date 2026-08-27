from fastapi import FastAPI

from atip_backend.api.v1.auth import router as auth_router
from atip_backend.api.v1.destinations import (
    router as destinations_router,
)
from atip_backend.api.v1.documents import (
    router as documents_router,
)
from atip_backend.core.config import get_settings


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    destinations_router,
    prefix="/api/v1",
)

app.include_router(
    documents_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}