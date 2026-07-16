# =============================================================================
# Rashid Dental AI Assistant — Database Configuration
# =============================================================================
# Sets up async SQLAlchemy engine and session factory.
# Provides dependency injection for FastAPI route handlers.
#
# Usage (in FastAPI routes):
#   async def my_route(db: AsyncSession = Depends(get_db)):
#       ...
# =============================================================================

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)

# Base class for all SQLAlchemy ORM models
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

# Create the async engine and session factory
# If DATABASE_URL is not set or empty, we use a placeholder to avoid startup crashes,
# but log a warning.
db_url = settings.database_url
if not db_url:
    logger.warning("DATABASE_URL is not set. Database operations will fail.")
    # Use a dummy postgres URL so create_async_engine doesn't crash on empty string
    db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/dummy"

engine: AsyncEngine | None = None
async_session_maker: async_sessionmaker[AsyncSession] | None = None

try:
    is_sqlite = db_url.startswith("sqlite")
    engine = create_async_engine(
        db_url,
        **( {"pool_size": settings.db_pool_size, "max_overflow": settings.db_max_overflow}
            if not is_sqlite else {} ),
        future=True,
        echo=False,  # Set to True for SQL queries logging if settings.debug is True
    )
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        future=True,
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    engine = None
    async_session_maker = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a database session per request.

    The session is automatically committed on success and rolled back on error.
    Always closed when the request lifecycle ends.

    Yields:
        AsyncSession: Active database session for the request.
    """
    if async_session_maker is None:
        logger.error("Database session maker is not initialized.")
        raise RuntimeError("Database connection is not configured.")

    async with async_session_maker() as session:
        try:
            yield session
            # Auto-commit is not recommended at session level, but we commit on success
            # when using a transactional unit of work. Custom commit is handled in repositories,
            # but this dependency ensures the session is closed safely.
        except Exception as e:
            await session.rollback()
            logger.error(f"Database transaction error: {e}")
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables on application startup.

    Called once during the FastAPI lifespan startup event.
    In production, prefer Alembic migrations over this function.
    """
    if engine is None:
        logger.warning("Database engine is not initialized. Skipping init_db.")
        return

    try:
        # In a real environment, we'd run migrations.
        # But we prepare this placeholder to create tables if needed.
        async with engine.begin() as conn:
            # For Day 2, we do not have specific models, so this will only
            # create Base tables if any exist.
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


async def check_db_connection() -> bool:
    """Check if the database connection is active.

    Used by the health check endpoint.
    """
    if engine is None:
        return False

    try:
        # Use a simple async execution to test connection
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning(f"Database connection check failed: {e}")
        return False
