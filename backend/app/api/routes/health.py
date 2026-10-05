from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "tailgate-quote"}


@router.get("/health/ready")
async def ready():
    return {"status": "ready"}