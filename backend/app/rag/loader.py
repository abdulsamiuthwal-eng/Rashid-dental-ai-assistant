# =============================================================================
# Rashid Dental AI Assistant — Markdown Loader
# =============================================================================
# Discovers and reads every .md file from the knowledge-base directory.
# Returns raw document content alongside basic file metadata.
# =============================================================================

from __future__ import annotations

import os
from pathlib import Path
from typing import NamedTuple

from backend.app.core.logging import get_logger

logger = get_logger(__name__)

# Supported file extension
_SUPPORTED_EXTENSION = ".md"


class RawDocument(NamedTuple):
    """Holds the raw text and metadata of a single knowledge-base file.

    Attributes:
        filename: Basename of the file (e.g. ``services.md``).
        filepath: Absolute path to the file.
        content: Full UTF-8 text of the file.
        size_bytes: File size in bytes.
        mtime: Last-modified timestamp (Unix epoch float).
    """

    filename: str
    filepath: Path
    content: str
    size_bytes: int
    mtime: float


class MarkdownLoader:
    """Discovers and loads Markdown files from a directory.

    The loader scans the given directory (non-recursively by default) for
    files ending in ``.md``, reads them as UTF-8, and returns a list of
    :class:`RawDocument` objects.

    Args:
        kb_dir: Path to the knowledge-base directory.
        recursive: If ``True``, scan sub-directories as well.
    """

    def __init__(self, kb_dir: str | Path, *, recursive: bool = False) -> None:
        """Initialise the loader with the given directory path."""
        self._kb_dir = Path(kb_dir).resolve()
        self._recursive = recursive

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_all(self) -> list[RawDocument]:
        """Load every supported Markdown file from the knowledge-base directory.

        Returns:
            A list of :class:`RawDocument` instances, one per file.

        Raises:
            FileNotFoundError: If ``kb_dir`` does not exist.
        """
        if not self._kb_dir.exists():
            raise FileNotFoundError(
                f"Knowledge-base directory not found: {self._kb_dir}"
            )

        paths = self._discover_files()
        documents: list[RawDocument] = []

        for path in sorted(paths):
            doc = self._read_file(path)
            if doc is not None:
                documents.append(doc)

        logger.info(
            f"Loaded {len(documents)} markdown document(s) from {self._kb_dir}"
        )
        return documents

    def get_directory_mtime(self) -> float:
        """Return the most-recent modification time of any .md file in kb_dir.

        Returns:
            Unix epoch float of the newest file, or 0.0 if no files found.
        """
        paths = self._discover_files()
        if not paths:
            return 0.0
        return max(p.stat().st_mtime for p in paths)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _discover_files(self) -> list[Path]:
        """Return all .md file paths in the knowledge-base directory."""
        if self._recursive:
            paths = list(self._kb_dir.rglob(f"*{_SUPPORTED_EXTENSION}"))
        else:
            paths = list(self._kb_dir.glob(f"*{_SUPPORTED_EXTENSION}"))

        unsupported = [
            f.name
            for f in self._kb_dir.iterdir()
            if f.is_file() and f.suffix != _SUPPORTED_EXTENSION
        ]
        if unsupported:
            logger.warning(
                f"Ignoring {len(unsupported)} unsupported file(s): {unsupported}"
            )

        return paths

    def _read_file(self, path: Path) -> RawDocument | None:
        """Read a single Markdown file and return a RawDocument.

        Args:
            path: Path to the file.

        Returns:
            A :class:`RawDocument` on success, or ``None`` on read error.
        """
        try:
            stat = os.stat(path)
            content = path.read_text(encoding="utf-8")
            return RawDocument(
                filename=path.name,
                filepath=path,
                content=content,
                size_bytes=stat.st_size,
                mtime=stat.st_mtime,
            )
        except OSError as exc:
            logger.error(f"Failed to read {path.name}: {exc}")
            return None
