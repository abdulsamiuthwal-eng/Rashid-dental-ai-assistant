# =============================================================================
# Rashid Dental AI Assistant — Markdown Cleaner
# =============================================================================
# Cleans raw Markdown text for embedding without destroying document structure.
#
# Preserved:  headings, bullet lists, numbered lists, tables, paragraphs.
# Removed:    HTML tags, image syntax, link URLs, excessive blank lines,
#             horizontal rules, inline code backtick fences.
# =============================================================================

from __future__ import annotations

import re


class MarkdownCleaner:
    """Cleans raw Markdown text for downstream chunking and embedding.

    The cleaner strips non-semantic noise (HTML, image syntax, raw URLs)
    while preserving headings, lists, tables, and paragraph structure so
    that the chunker can still split on heading boundaries.

    Usage::

        cleaner = MarkdownCleaner()
        clean_text = cleaner.clean(raw_markdown)
    """

    # ------------------------------------------------------------------
    # Compiled patterns (class-level — built once)
    # ------------------------------------------------------------------

    # HTML tags: <br>, <div class="x">, </span>, etc.
    _RE_HTML_TAG = re.compile(r"<[^>]+>", re.DOTALL)

    # Markdown image syntax: ![alt](url)
    _RE_IMAGE = re.compile(r"!\[.*?\]\(.*?\)", re.DOTALL)

    # Markdown link syntax → keep label text, discard URL: [label](url)
    _RE_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)", re.DOTALL)

    # Inline code spans: `some code` (keep content, remove backticks)
    _RE_INLINE_CODE = re.compile(r"`([^`\n]+)`")

    # Fenced code blocks: ```lang ... ``` or ~~~ ... ~~~
    _RE_CODE_FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)

    # Horizontal rules: ---, ***, ___
    _RE_HR = re.compile(r"^\s*[-*_]{3,}\s*$", re.MULTILINE)

    # HTML entities: &amp; &nbsp; &#160; etc.
    _RE_HTML_ENTITY = re.compile(r"&[a-zA-Z#0-9]+;")

    # Trailing whitespace on each line
    _RE_TRAILING_WS = re.compile(r"[ \t]+$", re.MULTILINE)

    # More than two consecutive blank lines → reduce to two
    _RE_MULTI_BLANK = re.compile(r"\n{3,}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def clean(self, text: str) -> str:
        """Apply all cleaning steps to raw Markdown text.

        Args:
            text: Raw Markdown string.

        Returns:
            Cleaned text with structure preserved and noise removed.
        """
        text = self._remove_code_fences(text)
        text = self._remove_images(text)
        text = self._simplify_links(text)
        text = self._remove_html_tags(text)
        text = self._remove_html_entities(text)
        text = self._simplify_inline_code(text)
        text = self._remove_horizontal_rules(text)
        text = self._normalize_whitespace(text)
        return text.strip()

    # ------------------------------------------------------------------
    # Private step methods
    # ------------------------------------------------------------------

    def _remove_code_fences(self, text: str) -> str:
        """Remove fenced code blocks entirely."""
        return self._RE_CODE_FENCE.sub("", text)

    def _remove_images(self, text: str) -> str:
        """Remove image syntax (``![alt](url)``)."""
        return self._RE_IMAGE.sub("", text)

    def _simplify_links(self, text: str) -> str:
        """Replace ``[label](url)`` with just the label text."""
        return self._RE_LINK.sub(r"\1", text)

    def _remove_html_tags(self, text: str) -> str:
        """Strip all HTML tags."""
        return self._RE_HTML_TAG.sub("", text)

    def _remove_html_entities(self, text: str) -> str:
        """Replace common HTML entities with a space."""
        return self._RE_HTML_ENTITY.sub(" ", text)

    def _simplify_inline_code(self, text: str) -> str:
        """Unwrap inline code spans — keep content, remove backticks."""
        return self._RE_INLINE_CODE.sub(r"\1", text)

    def _remove_horizontal_rules(self, text: str) -> str:
        """Remove Markdown horizontal rules (``---``, ``***``, etc.)."""
        return self._RE_HR.sub("", text)

    def _normalize_whitespace(self, text: str) -> str:
        """Trim trailing whitespace per line and collapse excess blank lines."""
        text = self._RE_TRAILING_WS.sub("", text)
        text = self._RE_MULTI_BLANK.sub("\n\n", text)
        return text
