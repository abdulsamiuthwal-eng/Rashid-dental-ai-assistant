import pytest
from backend.app.exceptions.exceptions import (
    AIServiceError,
    AppBaseException,
    AuthenticationError,
    DatabaseError,
    KnowledgeBaseError,
    NotFoundError,
    PromptInjectionError,
    RateLimitError,
    ValidationError,
    VectorStoreError,
)


def test_base_exception():
    exc = AppBaseException("Test error", error_code="TEST", status_code=400)
    assert exc.message == "Test error"
    assert exc.error_code == "TEST"
    assert exc.status_code == 400


def test_validation_error():
    exc = ValidationError("Invalid input")
    assert exc.status_code == 422
    assert exc.error_code == "VALIDATION_ERROR"


def test_not_found_error():
    exc = NotFoundError("Appointment", 42)
    assert exc.status_code == 404
    assert "42" in exc.message


def test_rate_limit_error():
    exc = RateLimitError()
    assert exc.status_code == 429
    assert exc.error_code == "RATE_LIMIT_EXCEEDED"


def test_authentication_error():
    exc = AuthenticationError()
    assert exc.status_code == 401
    assert exc.error_code == "AUTHENTICATION_REQUIRED"


def test_prompt_injection_error():
    exc = PromptInjectionError()
    assert exc.status_code == 400
    assert exc.error_code == "PROMPT_INJECTION_DETECTED"


def test_ai_service_error():
    exc = AIServiceError()
    assert exc.status_code == 503
    assert exc.error_code == "AI_SERVICE_ERROR"


def test_vector_store_error():
    exc = VectorStoreError()
    assert exc.status_code == 500
    assert exc.error_code == "VECTOR_STORE_ERROR"


def test_knowledge_base_error():
    exc = KnowledgeBaseError()
    assert exc.status_code == 500
    assert exc.error_code == "KNOWLEDGE_BASE_ERROR"


def test_database_error():
    exc = DatabaseError()
    assert exc.status_code == 500
    assert exc.error_code == "DATABASE_ERROR"


def test_exception_with_details():
    exc = ValidationError("Bad data", details={"field": "email", "reason": "invalid format"})
    assert exc.details["field"] == "email"
    assert exc.details["reason"] == "invalid format"
