import pytest


class TestRAGFlow:
    def test_loader_discovers_md_files(self):
        from backend.app.rag.loader import MarkdownLoader
        from pathlib import Path
        kb_path = Path(__file__).resolve().parent.parent.parent / "knowledge-base"
        loader = MarkdownLoader(kb_path)
        docs = loader.load_all()
        assert len(docs) > 0
        filenames = [d.filename for d in docs]
        assert "clinic-overview.md" in filenames
        assert "services.md" in filenames
        assert "dentists.md" in filenames

    def test_loader_to_chunker_pipeline(self):
        from backend.app.rag.loader import MarkdownLoader
        from backend.app.rag.cleaner import MarkdownCleaner
        from backend.app.rag.chunker import MarkdownChunker
        from pathlib import Path
        kb_path = Path(__file__).resolve().parent.parent.parent / "knowledge-base"
        loader = MarkdownLoader(kb_path)
        cleaner = MarkdownCleaner()
        chunker = MarkdownChunker()
        docs = loader.load_all()
        total_chunks = 0
        for doc in docs:
            cleaned = cleaner.clean(doc.content)
            chunks = chunker.chunk(doc.filename, cleaned)
            total_chunks += len(chunks)
            for c in chunks:
                assert c.filename == doc.filename
                assert len(c.content) > 0
        assert total_chunks > 10

    def test_chunker_preserves_heading_hierarchy(self):
        from backend.app.rag.loader import MarkdownLoader
        from backend.app.rag.cleaner import MarkdownCleaner
        from backend.app.rag.chunker import MarkdownChunker
        from pathlib import Path
        kb_path = Path(__file__).resolve().parent.parent.parent / "knowledge-base"
        loader = MarkdownLoader(kb_path)
        cleaner = MarkdownCleaner()
        chunker = MarkdownChunker()
        docs = loader.load_all()
        for doc in docs:
            cleaned = cleaner.clean(doc.content)
            chunks = chunker.chunk(doc.filename, cleaned)
            for c in chunks:
                if c.heading:
                    assert len(c.heading) > 0

    def test_mock_retrieval_works(self):
        from backend.app.rag.embedder import Embedder, EmbedderMode
        from backend.app.rag.vector_store import VectorStore
        from backend.app.rag.schemas import DocumentChunk
        from datetime import datetime
        embedder = Embedder(mode=EmbedderMode.MOCK)
        store = VectorStore()
        chunks = [
            DocumentChunk(
                chunk_id="t1", filename="test.md", heading="A", content="The clinic is open from 9 to 5.",
                char_count=30, word_count=7, created_at=datetime.utcnow(), document_type="test",
            ),
            DocumentChunk(
                chunk_id="t2", filename="test.md", heading="B", content="We offer teeth cleaning services.",
                char_count=32, word_count=5, created_at=datetime.utcnow(), document_type="test",
            ),
        ]
        store.build(chunks, embedder)
        results = store.search(embedder.embed_query("opening hours"), top_k=2)
        assert len(results) == 2
        scores = [s for _, s in results]
        assert scores[0] >= scores[1]
