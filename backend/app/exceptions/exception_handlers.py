# =============================================================================
# Rashid Dental AI Assistant — Exception Handlers
# =============================================================================
# Registers exception handler hooks for FastAPI.
# Translates custom exceptions, Pydantic validation errors, and unhandled
# exceptions into consistent JSON error responses.
# =============================================================================

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.core.logging import get_logger
from backend.app.exceptions.exceptions import AppBaseException

logger = get_logger(__name__)


async def app_base_exception_handler(
    request: Request, exc: AppBaseException
) -> JSONResponse:
    """Handle all custom application exceptions (AppBaseException)."""
    logger.warning(
        f"Application error occurred: {exc.error_code} - {exc.message} "
        f"[Path: {request.url.path}, Details: {exc.details}]"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "detail": {
                "message": exc.message,
                "error_code": exc.error_code,
                "details": exc.details,
            }
        }),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle FastAPI RequestValidationError."""
    # Build detailed field-specific errors
    details = {}
    for error in exc.errors():
        # Get field name path, e.g. body.full_name
        loc = ".".join(str(x) for x in error.get("loc", []))
        details[loc] = error.get("msg", "Invalid value")

    logger.warning(
        f"Request validation failed [Path: {request.url.path}, Details: {details}]"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": {
                "message": "Request validation failed. Please check the provided fields.",
                "error_code": "VALIDATION_ERROR",
                "details": details,
            }
        }),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle Starlette/FastAPI default HTTPException."""
    logger.info(
        f"HTTP exception [Path: {request.url.path}, "
        f"Status: {exc.status_code}, Detail: {exc.detail}]"
    )
    # Map standard status codes to error codes
    error_code_mapping = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        429: "RATE_LIMIT_EXCEEDED",
    }
    error_code = error_code_mapping.get(exc.status_code, "HTTP_ERROR")

    # If exc.detail is a dictionary, use it as details, otherwise put it in message
    message = exc.detail if isinstance(exc.detail, str) else "An HTTP error occurred."
    details: dict[str, Any] = exc.detail if isinstance(exc.detail, dict) else {}

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "detail": {
                "message": message,
                "error_code": error_code,
                "details": details,
            }
        }),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unhandled standard exceptions.

    Never exposes internal error trace or messages to the API consumer.
    """
    logger.opt(exception=exc).error(
        f"Unhandled system exception occurred [Path: {request.url.path}]"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({
            "detail": {
                "message": "An unexpected server error occurred. Please try again later.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "details": {},
            }
        }),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers to the FastAPI app instance."""
    app.add_exception_handler(AppBaseException, app_base_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
