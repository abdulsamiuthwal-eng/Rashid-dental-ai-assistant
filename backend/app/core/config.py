# =============================================================================
# Rashid Dental AI Assistant — Application Configuration
# =============================================================================
# This module defines all application settings using Pydantic-Settings.
# Settings are loaded from environment variables (or .env file in development).
#
# Usage:
#   from backend.app.core.config import settings
#   print(settings.app_name)
#
# IMPORTANT: Never import this module at the package level in modules that
# are imported at application startup before the .env is loaded.
# =============================================================================

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All settings are validated at startup via Pydantic.
    Missing required settings will raise a clear error before the app starts.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Silently ignore unknown env vars
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    app_name: str = Field(
        default="Rashid Dental AI Assistant", description="Application display name"
    )
    app_version: str = Field(default="1.0.0", description="Application version string")
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Deployment environment",
    )
    app_host: str = Field(default="127.0.0.1", description="Server bind host")
    app_port: int = Field(default=8000, ge=1024, le=65535, description="Server bind port")
    debug: bool = Field(default=False, description="Enable debug mode (development only)")

    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    secret_key: str = Field(
        default="",
        description="Secret key for JWT signing — must be set in production",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT signing algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        description="JWT access token expiry in minutes",
    )
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5500"],
        description="CORS allowed origins",
    )

    # -------------------------------------------------------------------------
    # Google Gemini AI
    # -------------------------------------------------------------------------
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key — required for AI functionality",
    )
    gemini_model: str = Field(
        default="gemini-1.5-flash",
        description="Gemini model identifier",
    )
    gemini_max_output_tokens: int = Field(
        default=1024,
        ge=1,
        le=8192,
        description="Maximum tokens in LLM response",
    )
    gemini_temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="LLM generation temperature (0=deterministic, 1=creative)",
    )

    # -------------------------------------------------------------------------
    # Database — PostgreSQL
    # -------------------------------------------------------------------------
    database_url: str = Field(
        default="",
        description="Full PostgreSQL connection URL (asyncpg dialect)",
    )
    db_pool_size: int = Field(default=5, ge=1, description="Connection pool size")
    db_max_overflow: int = Field(default=10, ge=0, description="Max connection overflow")

    # -------------------------------------------------------------------------
    # Vector Store — FAISS
    # -------------------------------------------------------------------------
    faiss_index_path: str = Field(
        default="./backend/vector_store/faiss.index",
        description="File path for persisting FAISS index",
    )
    embedding_model: str = Field(
        default="models/embedding-001",
        description="Google embedding model identifier",
    )

    # -------------------------------------------------------------------------
    # Knowledge Base
    # -------------------------------------------------------------------------
    knowledge_base_path: str = Field(
        default="./knowledge-base",
        description="Directory path to Markdown knowledge base files",
    )
    chunk_size: int = Field(
        default=1000,
        ge=100,
        description="Text chunk size in characters for document splitting",
    )
    chunk_overlap: int = Field(
        default=200,
        ge=0,
        description="Character overlap between consecutive chunks",
    )

    # -------------------------------------------------------------------------
    # RAG Pipeline
    # -------------------------------------------------------------------------
    rag_top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of top documents to retrieve for context",
    )
    rag_similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for document retrieval",
    )
    rag_max_context_length: int = Field(
        default=4000,
        ge=100,
        description="Maximum character length of context passed to LLM",
    )

    # -------------------------------------------------------------------------
    # Conversation Memory
    # -------------------------------------------------------------------------
    conversation_memory_window: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum conversation turns to retain in memory",
    )
    conversation_session_ttl: int = Field(
        default=3600,
        ge=60,
        description="Session time-to-live in seconds",
    )

    # -------------------------------------------------------------------------
    # Rate Limiting
    # -------------------------------------------------------------------------
    rate_limit_chat_per_minute: int = Field(
        default=20,
        ge=1,
        description="Max chat requests per user per minute",
    )
    rate_limit_appointments_per_hour: int = Field(
        default=5,
        ge=1,
        description="Max appointment requests per user per hour",
    )

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Application log level",
    )
    log_dir: str = Field(default="./logs", description="Log file output directory")
    log_file: str = Field(default="app.log", description="Log file name")

    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str, info: object) -> str:
        """Enforce a non-empty secret key in non-development environments."""
        # Note: 'info' contains validated data; check app_env when available
        if len(v) < 32 and v != "":
            raise ValueError("SECRET_KEY must be at least 32 characters long.")
        return v

    @model_validator(mode="after")
    def validate_env_requirements(self) -> "Settings":
        """Validate settings requirements based on the environment.

        Ensures required secrets and database strings are set appropriately.
        """
        # Validate database url scheme if present
        if self.database_url:
            is_sqlite = self.database_url.startswith("sqlite+aiosqlite://")
            has_async_pg = self.database_url.startswith("postgresql+asyncpg://")
            has_pg = self.database_url.startswith("postgresql://")
            if not (has_async_pg or has_pg or is_sqlite):
                raise ValueError(
                    "DATABASE_URL must be a PostgreSQL or SQLite connection URL "
                    "(e.g. postgresql+asyncpg://... or sqlite+aiosqlite:///...)"
                )
            # Automatically convert postgresql:// to postgresql+asyncpg:// for async compatibility
            if has_pg:
                self.database_url = self.database_url.replace(
                    "postgresql://", "postgresql+asyncpg://", 1
                )

        # Enforce production/staging requirements
        if self.app_env in ("production", "staging"):
            if not self.secret_key or len(self.secret_key) < 32:
                raise ValueError(
                    "SECRET_KEY must be configured and at least 32 characters "
                    "long in production/staging."
                )
            if not self.database_url:
                raise ValueError("DATABASE_URL must be configured in production/staging.")
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY must be configured in production/staging.")

        return self

    # -------------------------------------------------------------------------
    # Computed Properties
    # -------------------------------------------------------------------------
    @property
    def is_production(self) -> bool:
        """True when running in the production environment."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """True when running in the development environment."""
        return self.app_env == "development"

    @property
    def api_v1_prefix(self) -> str:
        """Versioned API route prefix."""
        return "/api/v1"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the application settings singleton.

    Uses lru_cache to ensure the .env file is read only once per
    application lifetime, improving startup performance.

    Returns:
        Settings: Validated application configuration object.
    """
    return Settings()


# Module-level convenience alias for direct import
settings: Settings = get_settings()
