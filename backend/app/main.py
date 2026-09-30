from fastapi import FastAPI

from app.api.routes.catalog import router as catalog_router
from app.config import settings
from app.api.routes.quotes import router as quotes_router


app = FastAPI(
    title=settings.app_name,
    description="Voice-first AI quoting assistant for field service professionals.",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


app.include_router(catalog_router)
app.include_router(quotes_router)
