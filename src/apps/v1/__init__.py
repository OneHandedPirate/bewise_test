from fastapi import APIRouter

from .healthcheck.router import router as healthcheck_router
from .applications.router import router as applications_router


router = APIRouter(
    prefix="/api/v1",
)

router.include_router(healthcheck_router)
router.include_router(applications_router)
