import pytest

from backend.app.models.appointment import Appointment


def test_appointment_model_creation():
    from datetime import date
    apt = Appointment(
        patient_name="John Doe",
        contact_number="+1234567890",
        preferred_date=date(2026, 8, 1),
        preferred_time="morning",
        requested_service="Checkup",
        reason="Routine",
    )
    assert apt.patient_name == "John Doe"
    assert apt.status == "pending" or apt.status is None
    assert apt.preferred_time == "morning"


def test_appointment_repr():
    from datetime import date
    apt = Appointment(
        patient_name="Jane Smith",
        contact_number="+1234567890",
        preferred_date=date(2026, 8, 1),
        preferred_time="afternoon",
        requested_service="Cleaning",
        reason="Regular",
    )
    rep = repr(apt)
    assert "Appointment" in rep
    assert "Jane Smith" in rep
