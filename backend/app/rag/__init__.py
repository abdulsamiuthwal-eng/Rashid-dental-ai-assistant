# =============================================================================
# Rashid Dental AI Assistant — RAG Pipeline Package
# =============================================================================
# Exposes the main public interface of the retrieval pipeline.
# =============================================================================

from backend.app.rag.retriever import RetrievalEngine
from backend.app.rag.schemas import DocumentChunk, RetrievalResult
from backend.app.rag.vector_store import VectorStore

__all__ = [
    "DocumentChunk",
    "RetrievalEngine",
    "RetrievalResult",
    "VectorStore",
]
