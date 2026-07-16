# =============================================================================
# Rashid Dental AI Assistant — FAISS Vector Store
# =============================================================================
# Manages the FAISS index lifecycle:
#   - Build index from document chunks + embeddings
#   - Save index and chunk metadata to disk
#   - Load index from disk
#   - Auto-rebuild when knowledge-base files change
#   - Similarity search against stored vectors
# =============================================================================

from __future__ import annotations

import pickle
from pathlib import Path
from typing import TYPE_CHECKING

import faiss
import numpy as np
import numpy.typing as npt

from backend.app.core.logging import get_logger
from backend.app.rag.schemas import DocumentChunk

if TYPE_CHECKING:
    from backend.app.rag.embedder import Embedder

logger = get_logger(__name__)

# Default on-disk paths (relative to project root)
_DEFAULT_INDEX_PATH = Path("backend/vector_store/faiss.index")
_DEFAULT_META_PATH = Path("backend/vector_store/chunks.pkl")


class VectorStore:
    """Manages a FAISS inner-product index over :class:`DocumentChunk` embeddings.

    Uses ``IndexFlatIP`` (exact inner-product / cosine search after L2-normalisation)
    for high-quality retrieval with no approximation error.

    Args:
        index_path: Where to write/read the ``.index`` file.
        meta_path: Where to write/read the pickled chunk list.
    """

    def __init__(
        self,
        index_path: str | Path = _DEFAULT_INDEX_PATH,
        meta_path: str | Path = _DEFAULT_META_PATH,
    ) -> None:
        """Initialise paths and empty internal state."""
        self._index_path = Path(index_path)
        self._meta_path = Path(meta_path)
        self._index: faiss.IndexFlatIP | None = None
        self._chunks: list[DocumentChunk] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def is_loaded(self) -> bool:
        """Return True if the index is in memory."""
        return self._index is not None

    @property
    def chunk_count(self) -> int:
        """Number of chunks in the current index."""
        return len(self._chunks)

    def build(
        self,
        chunks: list[DocumentChunk],
        embedder: Embedder,
    ) -> None:
        """Build a FAISS index from chunks by generating embeddings.

        Args:
            chunks: List of document chunks to index.
            embedder: Embedder instance used to generate vectors.
        """
        if not chunks:
            logger.warning("build() called with empty chunk list — skipping.")
            return

        texts = [c.content for c in chunks]
        logger.info(f"Generating embeddings for {len(texts)} chunk(s)…")
        vectors = embedder.embed_documents(texts)

        matrix = self._to_matrix(vectors)
        faiss.normalize_L2(matrix)  # cosine similarity via inner product

        dim = matrix.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(matrix)  # type: ignore[arg-type]

        self._index = index
        self._chunks = chunks
        logger.info(f"FAISS index built: {index.ntotal} vector(s), dim={dim}")

    def save(self) -> None:
        """Persist the current index and chunk metadata to disk.

        Raises:
            RuntimeError: If the index has not been built yet.
        """
        if self._index is None:
            raise RuntimeError("Cannot save — no index built. Call build() first.")

        self._index_path.parent.mkdir(parents=True, exist_ok=True)
        self._meta_path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self._index, str(self._index_path))
        with self._meta_path.open("wb") as f:
            pickle.dump(self._chunks, f)

        logger.info(
            f"Index saved → {self._index_path} | Metadata → {self._meta_path}"
        )

    def load(self) -> bool:
        """Load index and metadata from disk.

        Returns:
            ``True`` on success, ``False`` if files do not exist.
        """
        if not self._index_path.exists() or not self._meta_path.exists():
            logger.warning(
                "Index files not found — run build_index.py to create them."
            )
            return False

        self._index = faiss.read_index(str(self._index_path))
        with self._meta_path.open("rb") as f:
            self._chunks = pickle.load(f)  # noqa: S301  # trusted internal file

        logger.info(
            f"Index loaded: {self._index.ntotal} vector(s), "
            f"{len(self._chunks)} chunk(s)"
        )
        return True

    def auto_rebuild_if_stale(
        self,
        kb_dir: str | Path,
        embedder: Embedder,
        loader: object | None = None,
    ) -> bool:
        """Rebuild the index if any knowledge-base file is newer than the index.

        Args:
            kb_dir: Knowledge-base directory to check for changes.
            embedder: Embedder instance for rebuilding.
            loader: Optional pre-configured :class:`MarkdownLoader`. If ``None``,
                a default loader is created internally.

        Returns:
            ``True`` if the index was rebuilt, ``False`` if it was up-to-date.
        """
        from backend.app.rag.chunker import MarkdownChunker
        from backend.app.rag.cleaner import MarkdownCleaner
        from backend.app.rag.loader import MarkdownLoader

        kb_path = Path(kb_dir)
        md_loader = loader or MarkdownLoader(kb_path)  # type: ignore[arg-type]

        # Compare newest .md mtime vs index mtime
        if self._index_path.exists():
            index_mtime = self._index_path.stat().st_mtime
            # get_directory_mtime is defined on MarkdownLoader
            if hasattr(md_loader, "get_directory_mtime"):
                kb_mtime = md_loader.get_directory_mtime()  # type: ignore[union-attr]
            else:
                kb_mtime = max(
                    p.stat().st_mtime for p in kb_path.glob("*.md")
                ) if list(kb_path.glob("*.md")) else 0.0

            if kb_mtime <= index_mtime:
                logger.info("Index is up-to-date. No rebuild needed.")
                return False

        logger.info("Knowledge-base changed — rebuilding index…")

        cleaner = MarkdownCleaner()
        chunker = MarkdownChunker()
        raw_docs = md_loader.load_all()  # type: ignore[union-attr]

        all_chunks: list[DocumentChunk] = []
        for doc in raw_docs:
            cleaned = cleaner.clean(doc.content)
            all_chunks.extend(chunker.chunk(doc.filename, cleaned))

        self.build(all_chunks, embedder)
        self.save()
        return True

    def search(
        self, query_vector: list[float], top_k: int = 5
    ) -> list[tuple[DocumentChunk, float]]:
        """Search the index for the most similar chunks.

        Args:
            query_vector: Embedding of the user query.
            top_k: Maximum number of results to return.

        Returns:
            List of (chunk, score) tuples sorted by descending similarity.

        Raises:
            RuntimeError: If the index is not loaded or built.
        """
        if self._index is None:
            raise RuntimeError(
                "Index is not loaded. Call load() or build() first."
            )

        matrix = self._to_matrix([query_vector])
        faiss.normalize_L2(matrix)

        actual_k = min(top_k, self._index.ntotal)
        distances, indices = self._index.search(matrix, actual_k)  # type: ignore[arg-type]

        results: list[tuple[DocumentChunk, float]] = []
        for dist, idx in zip(distances[0], indices[0], strict=False):
            if idx == -1:  # FAISS sentinel for "no result"
                continue
            results.append((self._chunks[int(idx)], float(dist)))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_matrix(vectors: list[list[float]]) -> npt.NDArray[np.float32]:
        """Convert a list of float vectors to a float32 numpy matrix.

        Args:
            vectors: List of embedding vectors.

        Returns:
            2-D numpy array of shape (n, dim) with dtype float32.
        """
        return np.array(vectors, dtype=np.float32)
