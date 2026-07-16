# =============================================================================
# Rashid Dental AI Assistant — Custom Exception Classes
# =============================================================================
# Centralised exception hierarchy for the application.
# All custom exceptions should inherit from AppBaseException.
#
# Design principles:
#   - Structured exceptions carry HTTP status codes and error codes
#   - Error codes are machine-readable identifiers (e.g., "VALIDATION_ERROR")
#   - Error messages are human-readable (safe to expose to API consumers)
#   - Internal details (stack traces, DB errors) are NEVER exposed to clients
# =============================================================================

from typing import Any


class AppBaseException(Exception):  # noqa: N818
    """Base class for all Rashid Dental AI Assistant application exceptions.

    All custom exceptions should inherit from this class to enable
    centralized error handling in FastAPI exception handlers.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def __repr__(self) -> str:
        """Return a string representation of the exception."""
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"error_code={self.error_code!r}, "
            f"status_code={self.status_code})"
        )


# -----------------------------------------------------------------------------
# Client Errors (4xx)
# -----------------------------------------------------------------------------

class ValidationError(AppBaseException):
    """Raised when request data fails validation (422)."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class NotFoundError(AppBaseException):
    """Raised when a requested resource does not exist (404)."""

    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(
            message=f"{resource} with identifier '{identifier}' was not found.",
            error_code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": str(identifier)},
        )


class RateLimitError(AppBaseException):
    """Raised when a client exceeds the rate limit (429)."""

    def __init__(self, limit: str = "Request limit exceeded.") -> None:
        super().__init__(
            message=f"Too many requests. {limit} Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )


class AuthenticationError(AppBaseException):
    """Raised when authentication fails (401)."""

    def __init__(self, message: str = "Authentication required.") -> None:
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_REQUIRED",
            status_code=401,
        )


class PromptInjectionError(AppBaseException):
    """Raised when a prompt injection attempt is detected (400)."""

    def __init__(self) -> None:
        super().__init__(
            message=(
                "Your message could not be processed. "
                "Please ask a valid dental or clinic-related question."
            ),
            error_code="PROMPT_INJECTION_DETECTED",
            status_code=400,
        )


# -----------------------------------------------------------------------------
# Service Errors (5xx)
# -----------------------------------------------------------------------------

class AIServiceError(AppBaseException):
    """Raised when the Gemini AI service fails or returns an unexpected response."""

    def __init__(self, message: str = "The AI service is temporarily unavailable.") -> None:
        super().__init__(
            message=message,
            error_code="AI_SERVICE_ERROR",
            status_code=503,
        )


class VectorStoreError(AppBaseException):
    """Raised when FAISS vector store operations fail."""

    def __init__(self, message: str = "Vector store operation failed.") -> None:
        super().__init__(
            message=message,
            error_code="VECTOR_STORE_ERROR",
            status_code=500,
        )


class KnowledgeBaseError(AppBaseException):
    """Raised when knowledge base documents cannot be loaded or processed."""

    def __init__(self, message: str = "Knowledge base is unavailable.") -> None:
        super().__init__(
            message=message,
            error_code="KNOWLEDGE_BASE_ERROR",
            status_code=500,
        )


class DatabaseError(AppBaseException):
    """Raised when a database operation fails unexpectedly."""

    def __init__(self, message: str = "A database error occurred.") -> None:
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
        )
