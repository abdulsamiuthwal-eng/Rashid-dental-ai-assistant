from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator


class AppointmentRequest(BaseModel):
    patient_name: str = Field(
        min_length=1,
        max_length=200,
        description="Full name of the patient",
    )
    contact_number: str = Field(
        min_length=1,
        max_length=50,
        description="Contact phone number",
    )
    preferred_date: date = Field(description="Preferred appointment date")
    preferred_time: str = Field(
        min_length=1,
        max_length=20,
        description="Preferred time slot (e.g. Morning, Afternoon, Evening)",
    )
    requested_service: str = Field(
        min_length=1,
        max_length=200,
        description="Dental service requested",
    )
    reason: str = Field(
        min_length=1,
        max_length=2000,
        description="Short reason for the visit",
    )

    @field_validator("preferred_date")
    @classmethod
    def validate_date_not_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Preferred date must be today or in the future.")
        return v

    @field_validator("preferred_time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        allowed = {"morning", "afternoon", "evening"}
        if v.strip().lower() not in allowed:
            raise ValueError(
                f"Preferred time must be one of: {', '.join(sorted(allowed))}."
            )
        return v.strip().lower()


class AppointmentResponse(BaseModel):
    id: int = Field(description="Appointment record ID")
    patient_name: str = Field(description="Patient's full name")
    contact_number: str = Field(description="Contact phone number")
    preferred_date: date = Field(description="Preferred appointment date")
    preferred_time: str = Field(description="Preferred time slot")
    requested_service: str = Field(description="Dental service requested")
    reason: str = Field(description="Reason for visit")
    status: str = Field(description="Appointment status (e.g. pending)")
    message: str = Field(
        description="Confirmation message for the patient",
    )
