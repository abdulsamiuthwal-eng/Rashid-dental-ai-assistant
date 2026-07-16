from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.logging import get_logger
from backend.app.models.appointment import Appointment
from backend.app.schemas.appointment import AppointmentRequest

logger = get_logger(__name__)


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: AppointmentRequest) -> Appointment:
        appointment = Appointment(
            patient_name=data.patient_name.strip(),
            contact_number=data.contact_number.strip(),
            preferred_date=data.preferred_date,
            preferred_time=data.preferred_time.strip().lower(),
            requested_service=data.requested_service.strip(),
            reason=data.reason.strip(),
            status="pending",
        )
        self._session.add(appointment)
        await self._session.commit()
        await self._session.refresh(appointment)
        logger.info(f"Appointment created: id={appointment.id}, patient={appointment.patient_name}")
        return appointment

    async def get_by_id(self, appointment_id: int) -> Appointment | None:
        result = await self._session.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, limit: int = 50, offset: int = 0) -> list[Appointment]:
        result = await self._session.execute(
            select(Appointment)
            .order_by(Appointment.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
