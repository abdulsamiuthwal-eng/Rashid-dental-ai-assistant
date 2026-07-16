from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.logging import get_logger
from backend.app.core.security import decode_access_token
from backend.app.schemas.appointment import AppointmentRequest, AppointmentResponse
from backend.app.services.appointment.service import AppointmentService

logger = get_logger(__name__)

router = APIRouter()
security = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials | None = Security(security)):
    if credentials is None:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
        return payload
    except Exception:
        return None


@router.post(
    "/appointments",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit an appointment request",
)
async def create_appointment(
    body: AppointmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict[str, Any] | None = Depends(get_current_user),
) -> dict[str, Any]:
    service = AppointmentService(db)
    try:
        result = await service.create_appointment(body)
        return result.model_dump()
    except Exception as exc:
        logger.error(f"Failed to create appointment: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to process appointment request. Please try again later.",
                "error_code": "INTERNAL_ERROR",
            },
        ) from exc


@router.get(
    "/appointments",
    response_model=list[AppointmentResponse],
    summary="List all appointment requests (admin only)",
)
async def list_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to access appointment records.",
        )
    service = AppointmentService(db)
    appointments = await service.list_appointments()
    return [a.model_dump() for a in appointments]
