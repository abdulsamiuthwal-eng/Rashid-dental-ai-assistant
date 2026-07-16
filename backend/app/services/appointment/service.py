from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.logging import get_logger
from backend.app.repositories.appointment import AppointmentRepository
from backend.app.schemas.appointment import AppointmentRequest, AppointmentResponse

_CONFIRMATION_MESSAGE: str = (
    "Your appointment request has been received successfully. "
    "Please note that this is only a request and is not confirmed "
    "until Rashid Dental Clinic staff review and approve it. "
    "The clinic will contact you to confirm your appointment."
)

logger = get_logger(__name__)


class AppointmentService:
    def __init__(self, session: AsyncSession) -> None:
        self._repository = AppointmentRepository(session)

    async def create_appointment(self, data: AppointmentRequest) -> AppointmentResponse:
        appointment = await self._repository.create(data)
        logger.info(
            f"Appointment request created: id={appointment.id}, "
            f"patient={appointment.patient_name}, "
            f"service={appointment.requested_service}"
        )
        return AppointmentResponse(
            id=appointment.id,
            patient_name=appointment.patient_name,
            contact_number=appointment.contact_number,
            preferred_date=appointment.preferred_date,
            preferred_time=appointment.preferred_time,
            requested_service=appointment.requested_service,
            reason=appointment.reason,
            status=appointment.status,
            message=_CONFIRMATION_MESSAGE,
        )

    async def list_appointments(self) -> list[AppointmentResponse]:
        appointments = await self._repository.list_all()
        return [
            AppointmentResponse(
                id=a.id,
                patient_name=a.patient_name,
                contact_number=a.contact_number,
                preferred_date=a.preferred_date,
                preferred_time=a.preferred_time,
                requested_service=a.requested_service,
                reason=a.reason,
                status=a.status,
                message=_CONFIRMATION_MESSAGE,
            )
            for a in appointments
        ]
