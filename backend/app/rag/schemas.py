# =============================================================================
# Rashid Dental AI Assistant — RAG Schemas
# =============================================================================
# Pydantic data contracts for the retrieval pipeline.
# All components share these models to ensure consistency across the pipeline.
# =============================================================================

from datetime import datetime

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """A single text chunk extracted from a knowledge-base document.

    Attributes:
        chunk_id: Unique identifier for this chunk.
        filename: Source markdown filename (basename only).
        heading: Top-level heading under which this chunk lives.
        subheading: Nested sub-heading, if present.
        content: Raw text content of this chunk.
        char_count: Character count of content.
        word_count: Word count of content.
        created_at: ISO timestamp when the chunk was created.
        document_type: Category of the source document (e.g., "services").
    """

    chunk_id: str = Field(description="Unique identifier: <filename>_<index>")
    filename: str = Field(description="Source .md basename, e.g. services.md")
    heading: str = Field(default="", description="Top-level heading")
    subheading: str = Field(default="", description="Sub-heading, if any")
    content: str = Field(description="Chunk text content")
    char_count: int = Field(description="Number of characters in content")
    word_count: int = Field(description="Number of words in content")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of chunk creation",
    )
    document_type: str = Field(
        default="general",
        description="Derived from filename stem (e.g. 'services', 'pricing')",
    )


class RetrievalResult(BaseModel):
    """A single retrieval result returned by the semantic search engine.

    Attributes:
        chunk: The matched DocumentChunk.
        score: Cosine similarity score (higher = more relevant).
        rank: 1-based ranking position in the result list.
    """

    chunk: DocumentChunk
    score: float = Field(description="Similarity score (0.0 – 1.0)")
    rank: int = Field(description="1-based rank among returned results")


class RetrievalRequest(BaseModel):
    """Input model for a retrieval query.

    Attributes:
        query: The user's natural-language question.
        top_k: Maximum number of chunks to return.
    """

    query: str = Field(min_length=1, description="Natural-language query string")
    top_k: int = Field(default=5, ge=1, le=20, description="Max results to return")
