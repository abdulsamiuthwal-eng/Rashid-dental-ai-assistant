# =============================================================================
# Rashid Dental AI Assistant — Heading-Based Chunker
# =============================================================================
# Splits cleaned Markdown text into semantic chunks using heading boundaries.
#
# Strategy:
#   - Split on H1/H2/H3 headings (lines starting with #, ##, ###).
#   - Each chunk owns: its heading, the nearest parent heading as subheading,
#     and the text until the next heading.
#   - Chunks shorter than MIN_CHUNK_CHARS are merged into the previous chunk.
# =============================================================================

from __future__ import annotations

import re
import uuid
from datetime import datetime
from pathlib import Path

from backend.app.core.logging import get_logger
from backend.app.rag.schemas import DocumentChunk

logger = get_logger(__name__)

# Minimum characters a chunk must have to stand alone
_MIN_CHUNK_CHARS = 50

# Regex to match any Markdown heading line (H1–H6)
_RE_HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


class MarkdownChunker:
    """Splits cleaned Markdown documents into heading-based chunks.

    Each chunk captures one logical section of the document:
    from a heading line to the start of the next heading.

    Args:
        min_chunk_chars: Sections shorter than this are merged with the
            previous chunk rather than emitted as standalone chunks.

    Usage::

        chunker = MarkdownChunker()
        chunks = chunker.chunk("services.md", cleaned_text)
    """

    def __init__(self, min_chunk_chars: int = _MIN_CHUNK_CHARS) -> None:
        """Initialise with minimum chunk character threshold."""
        self._min_chunk_chars = min_chunk_chars

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chunk(self, filename: str, text: str) -> list[DocumentChunk]:
        """Split a cleaned Markdown document into :class:`DocumentChunk` list.

        Args:
            filename: Basename of the source file (used in chunk metadata).
            text: Cleaned Markdown text.

        Returns:
            Ordered list of :class:`DocumentChunk` instances.
        """
        document_type = Path(filename).stem  # e.g. "services"
        raw_sections = self._split_by_headings(text)
        chunks = self._build_chunks(filename, document_type, raw_sections)

        logger.info(
            f"Chunked '{filename}' → {len(chunks)} chunk(s)"
        )
        return chunks

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _split_by_headings(
        self, text: str
    ) -> list[tuple[str, str, str]]:
        """Split text into (level_marker, heading_title, body) triples.

        Args:
            text: Cleaned Markdown text.

        Returns:
            List of (hashes, heading_text, body_text) tuples.
        """
        # Find all heading positions
        matches = list(_RE_HEADING.finditer(text))

        if not matches:
            # No headings — treat entire document as one unnamed section
            return [("", "Document", text.strip())]

        sections: list[tuple[str, str, str]] = []

        for i, match in enumerate(matches):
            level_marker = match.group(1)   # e.g. "##"
            heading_title = match.group(2).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()
            sections.append((level_marker, heading_title, body))

        # Prepend any text before the first heading
        preamble = text[: matches[0].start()].strip()
        if preamble:
            sections.insert(0, ("", "Preamble", preamble))

        return sections

    def _build_chunks(
        self,
        filename: str,
        document_type: str,
        sections: list[tuple[str, str, str]],
    ) -> list[DocumentChunk]:
        """Convert raw sections into DocumentChunk objects.

        Args:
            filename: Source filename for metadata.
            document_type: Derived from filename stem.
            sections: List of (marker, heading, body) triples.

        Returns:
            List of :class:`DocumentChunk` with full metadata.
        """
        chunks: list[DocumentChunk] = []
        current_h1 = ""
        now = datetime.utcnow()
        pending_body = ""
        pending_heading = ""
        pending_subheading = ""

        def _flush(
            body: str,
            heading: str,
            subheading: str,
            index: int,
        ) -> DocumentChunk | None:
            """Create a chunk from accumulated content."""
            content = body.strip()
            if not content:
                return None
            chunk_id = f"{Path(filename).stem}_{index}_{uuid.uuid4().hex[:8]}"
            return DocumentChunk(
                chunk_id=chunk_id,
                filename=filename,
                heading=heading,
                subheading=subheading,
                content=content,
                char_count=len(content),
                word_count=len(content.split()),
                created_at=now,
                document_type=document_type,
            )

        chunk_index = 0
        for marker, heading, body in sections:
            level = len(marker)  # 0 = preamble, 1 = H1, 2 = H2, etc.

            if level == 1:
                current_h1 = heading
                subheading = ""
            elif level >= 2:
                subheading = heading
            else:
                subheading = ""

            full_content = f"{'#' * level + ' ' if level else ''}{heading}\n\n{body}".strip()

            # Merge very short sections into the running buffer
            if len(full_content) < self._min_chunk_chars and chunks:
                # append to last chunk's content
                last = chunks[-1]
                merged_content = last.content + "\n\n" + full_content
                chunks[-1] = last.model_copy(
                    update={
                        "content": merged_content,
                        "char_count": len(merged_content),
                        "word_count": len(merged_content.split()),
                    }
                )
                continue

            chunk = _flush(full_content, current_h1 or heading, subheading, chunk_index)
            if chunk:
                chunks.append(chunk)
                chunk_index += 1

        # Flush any remaining pending content
        if pending_body:
            chunk = _flush(pending_body, pending_heading, pending_subheading, chunk_index)
            if chunk:
                chunks.append(chunk)

        return chunks
