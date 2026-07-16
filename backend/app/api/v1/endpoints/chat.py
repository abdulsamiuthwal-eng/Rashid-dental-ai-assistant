from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from backend.app.core.logging import get_logger
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.ai.memory import ConversationMemory
from backend.app.services.rag.rag_pipeline import RAGPipeline

logger = get_logger(__name__)

router = APIRouter()

_memory = ConversationMemory(
    persist_path=str(Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "sessions.json"),
)


def _get_pipeline(request: Request) -> RAGPipeline | None:
    pipeline: RAGPipeline | None = getattr(request.app.state, "rag_pipeline", None)
    return pipeline


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a message to the AI assistant",
)
async def chat(
    body: ChatRequest,
    pipeline: RAGPipeline | None = Depends(_get_pipeline),
) -> dict[str, Any]:
    message = body.message.strip()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Message must not be empty.", "error_code": "VALIDATION_ERROR"},
        )

    if pipeline is None:
        logger.error("Chat endpoint called but RAG pipeline is not initialized.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": (
                    "The AI assistant is currently unavailable. "
                    "Please ensure GEMINI_API_KEY is set and the FAISS index has been built."
                ),
                "error_code": "SERVICE_UNAVAILABLE",
            },
        )

    session_id = _memory.get_or_create_session(body.session_id)
    history = _memory.get_history(session_id)

    try:
        answer, sources = pipeline.query(message, conversation_history=history)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"RAG pipeline query failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An internal error occurred while processing your message.",
                "error_code": "INTERNAL_ERROR",
            },
        ) from exc

    _memory.add_message(session_id, "user", message)
    _memory.add_message(session_id, "assistant", answer)

    return ChatResponse(
        message=answer,
        session_id=session_id,
        sources=sources,
    ).model_dump()
