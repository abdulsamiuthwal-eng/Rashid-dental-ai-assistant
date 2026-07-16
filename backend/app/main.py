# =============================================================================
# Rashid Dental AI Assistant — Application Entry Point
# =============================================================================
# This module creates and configures the FastAPI application instance.
# It serves as the application factory — all configuration, middleware,
# router registration, and lifespan management happens here.
#
# Run with: uvicorn backend.app.main:app --reload
# =============================================================================

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.app.api.v1.endpoints.health import router as health_router
from backend.app.api.v1.middleware.logging_middleware import RequestLoggingMiddleware
from backend.app.api.v1.router import router as api_v1_router
from backend.app.core.config import settings
from backend.app.core.database import init_db
from backend.app.core.logging import configure_logging, get_logger
from backend.app.exceptions.exception_handlers import register_exception_handlers

logger = get_logger(__name__)


def get_rag_pipeline(request: Request) -> Any:
    return request.app.state.rag_pipeline


# -----------------------------------------------------------------------------
# Lifespan Context Manager
# -----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown lifecycle events."""
    configure_logging()
    logger.info("==================================================")
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Host/Port: {settings.app_host}:{settings.app_port}")
    logger.info("==================================================")

    await init_db()

    pipeline = await _init_rag_pipeline()
    application.state.rag_pipeline = pipeline

    logger.info(f"{settings.app_name} initialization completed successfully.")
    yield

    logger.info(f"Shutting down {settings.app_name}...")
    logger.info("Cleaned up resources successfully.")


async def _init_rag_pipeline() -> Any:
    from backend.app.rag.embedder import EmbedderMode
    from backend.app.rag.retriever import RetrievalEngine
    from backend.app.rag.vector_store import VectorStore
    from backend.app.services.ai.gemini_client import GeminiClient
    from backend.app.services.rag.rag_pipeline import RAGPipeline

    index_path = (
        Path(settings.faiss_index_path).resolve()
        if settings.faiss_index_path
        else Path("backend/vector_store/faiss.index")
    )
    meta_path = index_path.with_name("chunks.pkl")

    if settings.gemini_api_key:
        embedder_mode = EmbedderMode.LIVE
        api_key = settings.gemini_api_key
    else:
        embedder_mode = EmbedderMode.MOCK
        api_key = None
        logger.warning("GEMINI_API_KEY not set — using mock embeddings (offline mode)")

    try:
        store = VectorStore(index_path=index_path, meta_path=meta_path)
        loaded = store.load()
        if not loaded:
            logger.warning("FAISS index not found. Chat will fall back gracefully.")
            return None

        retriever = RetrievalEngine.from_store(
            vector_store=store,
            embedder_mode=embedder_mode,
            api_key=api_key,
            default_top_k=settings.rag_top_k,
        )
    except Exception as exc:
        logger.error(f"Failed to initialize retrieval engine: {exc}")
        return None

    if not settings.gemini_api_key:
        logger.warning("GEMINI_API_KEY not set — AI responses will be unavailable.")
        return None

    try:
        gemini = GeminiClient(
            api_key=settings.gemini_api_key,
            model_name=settings.gemini_model,
            max_output_tokens=settings.gemini_max_output_tokens,
            temperature=settings.gemini_temperature,
        )
    except Exception as exc:
        logger.error(f"Failed to initialize Gemini client: {exc}")
        return None

    return RAGPipeline(
        retriever=retriever,
        gemini_client=gemini,
        top_k=settings.rag_top_k,
        max_context_length=settings.rag_max_context_length,
    )


# -----------------------------------------------------------------------------
# Application Factory
# -----------------------------------------------------------------------------

def create_application() -> FastAPI:
    """FastAPI application factory.

    Creates and configures the FastAPI instance with:
    - Application metadata (title, version, docs URLs)
    - Lifespan context manager (startup/shutdown hooks)
    - CORS middleware
    - Request logging middleware
    - Custom exception handlers
    - API router registration

    Returns:
        FastAPI: Configured application instance.
    """
    application = FastAPI(
        title=settings.app_name,
        description=(
            "REST API for the Rashid Dental AI Assistant. "
            "Provides RAG-powered chat, appointment request collection, "
            "and clinic information retrieval."
        ),
        version=settings.app_version,
        docs_url="/docs",           # Swagger UI
        redoc_url="/redoc",         # ReDoc UI
        openapi_url="/openapi.json",
        lifespan=lifespan,
        contact={
            "name": "DEVFORGE Internship — Project 2",
        },
        license_info={
            "name": "MIT",
        },
    )

    from slowapi import Limiter
    from slowapi.util import get_remote_address

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{settings.rate_limit_chat_per_minute}/minute"],
    )
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    application.add_middleware(SlowAPIMiddleware)

    application.add_middleware(RequestLoggingMiddleware)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(application)

    application.include_router(health_router, prefix="/api")

    application.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    frontend_path = Path(__file__).resolve().parent.parent.parent / "frontend"
    if frontend_path.exists():
        application.mount(
            "/",
            StaticFiles(directory=str(frontend_path), html=True),
            name="frontend",
        )

    return application


# -----------------------------------------------------------------------------
# Application Instance
# -----------------------------------------------------------------------------

app: FastAPI = create_application()

