# =============================================================================
# Rashid Dental AI Assistant — Embedding Module
# =============================================================================
# Wraps Google's Generative AI embedding API (models/embedding-001).
#
# ⚠️  Requires GOOGLE_API_KEY in the environment / .env file.
#
# The embedder exposes two modes:
#   - live:  calls the real Google API (requires key)
#   - mock:  returns deterministic random vectors (for offline testing)
# =============================================================================

from __future__ import annotations

import hashlib
import os
import struct
import time
from enum import Enum
from typing import Final

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.app.core.logging import get_logger

logger = get_logger(__name__)

# Google embedding model to use
_EMBEDDING_MODEL: Final[str] = "models/gemini-embedding-001"

# Dimensionality of the Google embedding model output
_EMBEDDING_DIM: Final[int] = 768

# Task type for retrieval — as per Google API spec
_TASK_TYPE_DOC: Final[str] = "retrieval_document"
_TASK_TYPE_QUERY: Final[str] = "retrieval_query"

# Batch size — stay under API limits
_BATCH_SIZE: Final[int] = 50


class EmbedderMode(str, Enum):
    """Operating mode for the :class:`Embedder`."""

    LIVE = "live"
    MOCK = "mock"


class Embedder:
    """Generates dense vector embeddings using Google's embedding-001 model.

    Args:
        mode: ``EmbedderMode.LIVE`` to call the real API,
              ``EmbedderMode.MOCK`` for offline testing (returns random vectors).
        api_key: Google API key. Falls back to the ``GOOGLE_API_KEY`` env var.

    Raises:
        EnvironmentError: If ``mode=LIVE`` and no API key is available.
    """

    def __init__(
        self,
        mode: EmbedderMode = EmbedderMode.LIVE,
        api_key: str | None = None,
    ) -> None:
        """Initialise the embedder."""
        self._mode = mode

        if self._mode == EmbedderMode.LIVE:
            resolved_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
            if not resolved_key:
                raise OSError(
                    "GOOGLE_API_KEY or GEMINI_API_KEY is required for live embedding. "
                    "Add it to your .env file or pass api_key= directly."
                )
            genai.configure(api_key=resolved_key)
            logger.info(f"Embedder initialised in LIVE mode (model={_EMBEDDING_MODEL})")
        else:
            logger.warning(
                "Embedder running in MOCK mode — embeddings are random vectors. "
                "Set GOOGLE_API_KEY and use EmbedderMode.LIVE for production."
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def dimension(self) -> int:
        """Return the embedding vector dimension."""
        return _EMBEDDING_DIM

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of document texts in batches.

        Args:
            texts: List of plain-text strings to embed.

        Returns:
            List of float vectors, one per input text.
        """
        if self._mode == EmbedderMode.MOCK:
            return [self._mock_vector(t) for t in texts]

        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), _BATCH_SIZE):
            batch = texts[i : i + _BATCH_SIZE]
            batch_embeddings = self._embed_batch(batch, task_type=_TASK_TYPE_DOC)
            all_embeddings.extend(batch_embeddings)
            if i + _BATCH_SIZE < len(texts):
                time.sleep(0.1)  # gentle rate-limit backoff

        logger.info(f"Embedded {len(all_embeddings)} document(s)")
        return all_embeddings

    def embed_query(self, query: str) -> list[float]:
        """Embed a single user query string.

        Args:
            query: The query text.

        Returns:
            A single float vector of length :attr:`dimension`.
        """
        if self._mode == EmbedderMode.MOCK:
            return self._mock_vector(query)

        result = self._embed_batch([query], task_type=_TASK_TYPE_QUERY)
        return result[0]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _embed_batch(
        self, texts: list[str], task_type: str
    ) -> list[list[float]]:
        """Call the Google embedding API for a batch of texts.

        Args:
            texts: Batch of strings.
            task_type: ``"retrieval_document"`` or ``"retrieval_query"``.

        Returns:
            List of embedding vectors.
        """
        result = genai.embed_content(
            model=_EMBEDDING_MODEL,
            content=texts,
            task_type=task_type,
        )
        # result["embedding"] is a list of vectors when content is a list
        embeddings: list[list[float]] = result["embedding"]  # type: ignore[index]
        return embeddings

    @staticmethod
    def _mock_vector(text: str) -> list[float]:
        """Generate a deterministic pseudo-random vector from text hash.

        Uses SHA-256 of the input text to seed 768 float values in [-1, 1].

        Args:
            text: Input text.

        Returns:
            A deterministic float vector of length :data:`_EMBEDDING_DIM`.
        """
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Tile the digest to fill _EMBEDDING_DIM floats
        repeated = (digest * ((_EMBEDDING_DIM * 4 // len(digest)) + 1))[
            : _EMBEDDING_DIM * 4
        ]
        raw_ints = struct.unpack(f"{_EMBEDDING_DIM}I", repeated)
        # Normalise to [-1, 1]
        max_uint = 2**32 - 1
        return [(v / max_uint) * 2 - 1 for v in raw_ints]
