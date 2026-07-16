# =============================================================================
# Rashid Dental AI Assistant — Logging Configuration
# =============================================================================
# Sets up structured logging using Loguru.
# Implements: console output (development) + file rotation (production).
#
# Usage:
#   from backend.app.core.logging import get_logger
#   logger = get_logger(__name__)
#   logger.info("Server started")
# =============================================================================

import logging
import sys
import types
from pathlib import Path
from typing import Any

from loguru import logger

from backend.app.core.config import settings


class InterceptHandler(logging.Handler):
    """Default handler to intercept standard library logging messages.

    Redirects them to Loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """Emit the log record to Loguru."""
        # Get corresponding Loguru level if it exists
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame: types.FrameType | None = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back if frame else None
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure_logging() -> None:
    """Configure application-wide logging.

    Called once at application startup via the FastAPI lifespan manager.

    Behaviour:
        - Development: Human-readable coloured output to stdout, DEBUG/INFO level
        - Production: JSON-structured rotation to file, INFO level
    """
    # Remove default loguru handlers
    logger.remove()

    # Log format definition
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 1. Console Handler (stdout)
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=settings.debug,
        diagnose=settings.debug,
    )

    # 2. File Handler (rotated, retained)
    log_dir = Path(settings.log_dir)
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_filepath = log_dir / settings.log_file

        logger.add(
            str(log_filepath),
            format=log_format,
            level=settings.log_level,
            rotation="00:00",  # Rotates every day at midnight
            retention="30 days",  # Keep logs for 30 days
            compression="zip",  # Compress old log files
            backtrace=True,
            diagnose=settings.debug,
        )
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to setup file logger: {e}\n")

    # 3. Intercept standard library logging (uvicorn, fastapi, sqlalchemy)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Overwrite specific library logger configurations to propagate to our InterceptHandler
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "sqlalchemy.engine"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True


def get_logger(name: str) -> Any:  # noqa: ANN401
    """Return a contextual logger for the given module name.

    Args:
        name: Module name, typically passed as __name__.

    Returns:
        Logger instance bound to the given module name.
    """
    return logger.bind(module=name)
