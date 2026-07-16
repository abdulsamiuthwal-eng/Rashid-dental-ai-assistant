from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        description="User's message to the AI assistant",
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session identifier for conversation continuity",
    )

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message must not be empty or whitespace only.")
        return v.strip()


class SourceInfo(BaseModel):
    filename: str = Field(description="Source knowledge-base file name")
    heading: str = Field(description="Section heading from the source document")
    chunk_id: str = Field(description="Unique chunk identifier")


class ChatResponse(BaseModel):
    message: str = Field(description="AI assistant response text")
    session_id: str = Field(description="Session identifier for conversation continuity")
    sources: list[SourceInfo] = Field(
        description="List of knowledge-base sources used for the response",
    )
