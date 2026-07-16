from datetime import date, timedelta

import pytest

from backend.app.schemas.appointment import AppointmentRequest, AppointmentResponse


def test_appointment_request_valid():
    tomorrow = date.today() + timedelta(days=1)
    req = AppointmentRequest(
        patient_name="John Doe",
        contact_number="+1234567890",
        preferred_date=tomorrow,
        preferred_time="morning",
        requested_service="General Checkup",
        reason="Routine checkup",
    )
    assert req.patient_name == "John Doe"
    assert req.preferred_time == "morning"


def test_appointment_request_past_date_raises():
    yesterday = date.today() - timedelta(days=1)
    with pytest.raises(ValueError):
        AppointmentRequest(
            patient_name="John Doe",
            contact_number="+1234567890",
            preferred_date=yesterday,
            preferred_time="morning",
            requested_service="General Checkup",
            reason="Routine checkup",
        )


def test_appointment_request_invalid_time_raises():
    tomorrow = date.today() + timedelta(days=1)
    with pytest.raises(ValueError, match="Preferred time must be one of"):
        AppointmentRequest(
            patient_name="John Doe",
            contact_number="+1234567890",
            preferred_date=tomorrow,
            preferred_time="midnight",
            requested_service="General Checkup",
            reason="Routine checkup",
        )


def test_appointment_request_valid_time_variants():
    tomorrow = date.today() + timedelta(days=1)
    req_morning = AppointmentRequest(
        patient_name="A", contact_number="1", preferred_date=tomorrow,
        preferred_time="Morning", requested_service="C", reason="R",
    )
    assert req_morning.preferred_time == "morning"

    req_afternoon = AppointmentRequest(
        patient_name="A", contact_number="1", preferred_date=tomorrow,
        preferred_time="AFTERNOON", requested_service="C", reason="R",
    )
    assert req_afternoon.preferred_time == "afternoon"

    req_evening = AppointmentRequest(
        patient_name="A", contact_number="1", preferred_date=tomorrow,
        preferred_time="Evening", requested_service="C", reason="R",
    )
    assert req_evening.preferred_time == "evening"


def test_appointment_request_strips_whitespace():
    tomorrow = date.today() + timedelta(days=1)
    req = AppointmentRequest(
        patient_name="  John Doe  ",
        contact_number="  +1234567890  ",
        preferred_date=tomorrow,
        preferred_time="  morning  ",
        requested_service="  Checkup  ",
        reason="  Routine  ",
    )
    assert req.preferred_time == "morning"


def test_appointment_response_contains_message():
    response = AppointmentResponse(
        id=1,
        patient_name="John Doe",
        contact_number="+1234567890",
        preferred_date=date.today() + timedelta(days=1),
        preferred_time="morning",
        requested_service="General Checkup",
        reason="Routine checkup",
        status="pending",
        message="Your appointment request has been received.",
    )
    assert "received" in response.message
    assert response.status == "pending"
    assert response.id == 1


def test_appointment_request_empty_name_raises():
    tomorrow = date.today() + timedelta(days=1)
    with pytest.raises(ValueError):
        AppointmentRequest(
            patient_name="",
            contact_number="+1234567890",
            preferred_date=tomorrow,
            preferred_time="morning",
            requested_service="Checkup",
            reason="Routine",
        )
