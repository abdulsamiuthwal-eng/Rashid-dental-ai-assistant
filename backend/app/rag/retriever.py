# =============================================================================
# Rashid Dental AI Assistant — Retrieval Engine
# =============================================================================
# High-level interface for semantic retrieval over the knowledge base.
#
# Input:  User question (string)
# Output: Ranked list of RetrievalResult (chunk + score + rank + attribution)
#
# Does NOT call Gemini chat. Does NOT generate answers.
# =============================================================================

from __future__ import annotations

from pathlib import Path

from backend.app.core.logging import get_logger
from backend.app.rag.embedder import Embedder, EmbedderMode
from backend.app.rag.schemas import DocumentChunk, RetrievalResult
from backend.app.rag.vector_store import VectorStore

logger = get_logger(__name__)

# Default on-disk paths (must match VectorStore defaults)
_DEFAULT_INDEX_PATH = Path("backend/vector_store/faiss.index")
_DEFAULT_META_PATH = Path("backend/vector_store/chunks.pkl")


class RetrievalEngine:
    """Semantic retrieval engine over the knowledge-base FAISS index.

    Orchestrates embedding → search → result formatting.

    Args:
        embedder: :class:`Embedder` instance (live or mock).
        vector_store: :class:`VectorStore` instance with loaded index.
        default_top_k: Default number of results to return.

    Usage::

        engine = RetrievalEngine.from_disk()
        results = engine.retrieve("What are your clinic hours?", top_k=3)
        for r in results:
            print(r.rank, r.score, r.chunk.heading, r.chunk.filename)
    """

    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
        default_top_k: int = 5,
    ) -> None:
        """Initialise with pre-configured embedder and vector store."""
        self._embedder = embedder
        self._vector_store = vector_store
        self._default_top_k = default_top_k

    # ------------------------------------------------------------------
    # Factory constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_disk(
        cls,
        index_path: str | Path = _DEFAULT_INDEX_PATH,
        meta_path: str | Path = _DEFAULT_META_PATH,
        embedder_mode: EmbedderMode = EmbedderMode.LIVE,
        api_key: str | None = None,
        default_top_k: int = 5,
    ) -> RetrievalEngine:
        """Create an engine by loading the FAISS index from disk.

        Args:
            index_path: Path to the ``.index`` file.
            meta_path: Path to the ``.pkl`` metadata file.
            embedder_mode: ``LIVE`` requires ``GOOGLE_API_KEY``, ``MOCK`` works offline.
            api_key: Optional API key (falls back to env var).
            default_top_k: Default result count.

        Returns:
            A ready-to-use :class:`RetrievalEngine`.

        Raises:
            RuntimeError: If the index files are not found on disk.
        """
        embedder = Embedder(mode=embedder_mode, api_key=api_key)
        store = VectorStore(index_path=index_path, meta_path=meta_path)
        loaded = store.load()
        if not loaded:
            raise RuntimeError(
                "FAISS index not found. Run `python scripts/build_index.py` first."
            )
        return cls(embedder=embedder, vector_store=store, default_top_k=default_top_k)

    @classmethod
    def from_store(
        cls,
        vector_store: VectorStore,
        embedder_mode: EmbedderMode = EmbedderMode.LIVE,
        api_key: str | None = None,
        default_top_k: int = 5,
    ) -> RetrievalEngine:
        """Create an engine from an already-loaded :class:`VectorStore`.

        Args:
            vector_store: Pre-loaded vector store.
            embedder_mode: Operating mode for the embedder.
            api_key: Optional Google API key.
            default_top_k: Default result count.

        Returns:
            A ready-to-use :class:`RetrievalEngine`.
        """
        embedder = Embedder(mode=embedder_mode, api_key=api_key)
        return cls(embedder=embedder, vector_store=vector_store, default_top_k=default_top_k)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[RetrievalResult]:
        """Retrieve the most relevant knowledge-base chunks for a query.

        Args:
            query: User's natural-language question.
            top_k: Number of results to return. Defaults to ``default_top_k``.

        Returns:
            Ordered list of :class:`RetrievalResult` (rank 1 = most relevant).

        Raises:
            RuntimeError: If the vector store index is not loaded.
            ValueError: If the query string is empty.
        """
        if not query.strip():
            raise ValueError("Query string must not be empty.")

        k = top_k if top_k is not None else self._default_top_k

        logger.info(f"Retrieving top-{k} chunks for query: '{query[:80]}'")

        query_vector = self._embedder.embed_query(query)
        raw_results = self._vector_store.search(query_vector, top_k=k)

        results = [
            RetrievalResult(chunk=chunk, score=score, rank=rank)
            for rank, (chunk, score) in enumerate(raw_results, start=1)
        ]

        logger.info(
            f"Retrieved {len(results)} result(s) — "
            f"top score: {results[0].score:.4f}" if results else "no results"
        )
        return results

    def retrieve_with_attribution(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[dict[str, object]]:
        """Retrieve results with full source attribution metadata.

        Convenience wrapper that flattens each result into a plain dict
        including all source attribution fields (filename, heading, section,
        chunk_id) for downstream display.

        Args:
            query: User question.
            top_k: Max results.

        Returns:
            List of dicts with keys: rank, score, content, filename,
            heading, subheading, chunk_id, document_type.
        """
        results = self.retrieve(query, top_k=top_k)
        return [self._format_result(r) for r in results]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_result(result: RetrievalResult) -> dict[str, object]:
        """Flatten a RetrievalResult into a plain attribution dict.

        Args:
            result: A single retrieval result.

        Returns:
            Dict with all attribution and content fields.
        """
        chunk: DocumentChunk = result.chunk
        return {
            "rank": result.rank,
            "score": round(result.score, 6),
            "content": chunk.content,
            "filename": chunk.filename,
            "heading": chunk.heading,
            "subheading": chunk.subheading,
            "chunk_id": chunk.chunk_id,
            "document_type": chunk.document_type,
            "char_count": chunk.char_count,
            "word_count": chunk.word_count,
        }
