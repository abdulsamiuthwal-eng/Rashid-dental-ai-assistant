# =============================================================================
# Rashid Dental AI Assistant — API v1 Router
# =============================================================================
# Aggregates and prefixes all API v1 endpoints.
# =============================================================================

from fastapi import APIRouter

from backend.app.api.v1.endpoints.appointments import router as appointments_router
from backend.app.api.v1.endpoints.auth import router as auth_router
from backend.app.api.v1.endpoints.chat import router as chat_router
from backend.app.api.v1.endpoints.health import router as health_router

router = APIRouter()

router.include_router(health_router, tags=["Health"])
router.include_router(chat_router, tags=["Chat"])
router.include_router(appointments_router, tags=["Appointments"])
router.include_router(auth_router, tags=["Authentication"])
