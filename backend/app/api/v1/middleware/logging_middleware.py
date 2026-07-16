# =============================================================================
# Rashid Dental AI Assistant — Request Logging Middleware
# =============================================================================
# Implements custom ASGI middleware to log incoming HTTP requests,
# track response execution latencies, and output structured logs via Loguru.
# =============================================================================

import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request/response cycles.

    Tracks methods, paths, status codes, client IPs, and processing time.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request and log lifecycle performance details."""
        # Prevent logging sensitive fields or paths
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        query_params = str(request.query_params)

        start_time = time.perf_counter()

        # Log request receipt (excluding high-frequency health checks)
        # We will log it at debug level if health check, info otherwise
        if path == "/api/health":
            logger.debug(f"Request: {method} {path} - IP: {client_ip}")
        else:
            query_str = f" - Query: {query_params}" if query_params else ""
            logger.info(f"Request: {method} {path} - IP: {client_ip}{query_str}")

        try:
            response = await call_next(request)
        except Exception as e:
            # Calculate duration even in case of unhandled error
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"Request failed: {method} {path} - IP: {client_ip} - "
                f"Duration: {duration_ms:.2f}ms - Error: {e}"
            )
            # Re-raise so the unhandled exception handler captures it
            raise e

        duration_ms = (time.perf_counter() - start_time) * 1000

        # Add latency header to the response (useful for debugging/inspection)
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"

        log_msg = (
            f"Response: {method} {path} - Status: {response.status_code} - "
            f"Duration: {duration_ms:.2f}ms"
        )
        if response.status_code >= 500:
            logger.error(log_msg)
        elif response.status_code >= 400:
            logger.warning(log_msg)
        else:
            if path == "/api/health":
                logger.debug(log_msg)
            else:
                logger.info(log_msg)

        return response
