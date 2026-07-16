from pathlib import Path

import pytest

from backend.app.rag.chunker import MarkdownChunker
from backend.app.rag.cleaner import MarkdownCleaner
from backend.app.rag.schemas import DocumentChunk


def test_cleaner_removes_html_tags():
    cleaner = MarkdownCleaner()
    result = cleaner.clean("<div>Hello <b>World</b></div>")
    assert "<div>" not in result
    assert "<b>" not in result
    assert "Hello World" in result


def test_cleaner_simplifies_links():
    cleaner = MarkdownCleaner()
    result = cleaner.clean("Click [here](https://example.com) for info")
    assert "https://example.com" not in result
    assert "Click here for info" in result


def test_cleaner_removes_images():
    cleaner = MarkdownCleaner()
    result = cleaner.clean("![alt](image.png)")
    assert "image.png" not in result


def test_cleaner_preserves_headings():
    cleaner = MarkdownCleaner()
    result = cleaner.clean("# Heading 1\n\nSome text\n\n## Heading 2\n\nMore text")
    assert "# Heading 1" in result
    assert "## Heading 2" in result


def test_cleaner_normalizes_whitespace():
    cleaner = MarkdownCleaner()
    result = cleaner.clean("Line 1\n\n\n\nLine 2")
    assert "\n\n\n\n" not in result


def test_chunker_splits_on_headings():
    chunker = MarkdownChunker(min_chunk_chars=10)
    text = "# Title\n\n" + "A" * 50 + "\n\n## Section 1\n\n" + "B" * 50 + "\n\n## Section 2\n\n" + "C" * 50
    chunks = chunker.chunk("test.md", text)
    assert len(chunks) >= 2


def test_chunker_metadata():
    chunker = MarkdownChunker()
    text = "# Services\n\nWe offer dental services.\n\n## General\n\nCheckups and cleaning."
    chunks = chunker.chunk("services.md", text)
    for c in chunks:
        assert c.filename == "services.md"
        assert c.document_type == "services"
        assert c.chunk_id.startswith("services_")
        assert c.char_count > 0
        assert c.word_count > 0


def test_chunker_merges_short_sections():
    chunker = MarkdownChunker(min_chunk_chars=100)
    text = "# Big Section\n\n" + "A" * 200 + "\n\n## Tiny\n\nsmall"
    chunks = chunker.chunk("test.md", text)
    # Tiny section should be merged into Big Section
    assert len(chunks) == 1


def test_document_chunk_creation():
    from datetime import datetime
    chunk = DocumentChunk(
        chunk_id="test_0_abc",
        filename="test.md",
        heading="Test",
        content="Hello world",
        char_count=11,
        word_count=2,
        created_at=datetime.utcnow(),
        document_type="test",
    )
    assert chunk.chunk_id == "test_0_abc"
    assert chunk.content == "Hello world"
    assert chunk.char_count == 11
    assert chunk.word_count == 2
    assert chunk.document_type == "test"


def test_mock_embedder_dimension():
    from backend.app.rag.embedder import Embedder, EmbedderMode
    embedder = Embedder(mode=EmbedderMode.MOCK)
    assert embedder.dimension == 768


def test_mock_embedder_returns_vector():
    from backend.app.rag.embedder import Embedder, EmbedderMode
    embedder = Embedder(mode=EmbedderMode.MOCK)
    vector = embedder.embed_query("test")
    assert len(vector) == 768
    assert all(isinstance(v, float) for v in vector)


def test_mock_embedder_deterministic():
    from backend.app.rag.embedder import Embedder, EmbedderMode
    embedder = Embedder(mode=EmbedderMode.MOCK)
    v1 = embedder.embed_query("hello world")
    v2 = embedder.embed_query("hello world")
    assert v1 == v2


def test_mock_embedder_embed_documents():
    from backend.app.rag.embedder import Embedder, EmbedderMode
    embedder = Embedder(mode=EmbedderMode.MOCK)
    vectors = embedder.embed_documents(["doc1", "doc2", "doc3"])
    assert len(vectors) == 3
    assert len(vectors[0]) == 768
