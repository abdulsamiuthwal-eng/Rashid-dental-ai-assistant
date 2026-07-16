# =============================================================================
# Rashid Dental AI Assistant — Health Check Endpoint
# =============================================================================
# Implements health status checks for the API and dependent services (Database).
# =============================================================================

import time
from typing import Any

from fastapi import APIRouter, status

from backend.app.core.config import settings
from backend.app.core.database import check_db_connection

router = APIRouter()

# Keep track of startup time to compute uptime
START_TIME = time.time()


@router.get("/health", status_code=status.HTTP_200_OK, summary="Get API Health Status")
async def get_health() -> dict[str, Any]:
    """Get health status of the application, version, uptime, and database."""
    uptime_seconds = time.time() - START_TIME
    db_connected = await check_db_connection()

    # Determine overall status
    overall_status = "healthy"
    if not db_connected:
        overall_status = "unhealthy"

    return {
        "status": overall_status,
        "version": settings.app_version,
        "environment": settings.app_env,
        "uptime_seconds": round(uptime_seconds, 2),
        "database": "connected" if db_connected else "disconnected",
    }
