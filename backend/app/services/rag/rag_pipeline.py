from __future__ import annotations

from backend.app.core.logging import get_logger
from backend.app.core.system_prompt import (
    CONTEXT_TEMPLATE,
    INJECTION_REFUSAL,
    NO_CONTEXT_FALLBACK,
    SYSTEM_INFO_REFUSAL,
    SYSTEM_PROMPT,
)
from backend.app.exceptions.exceptions import AIServiceError, VectorStoreError
from backend.app.rag.retriever import RetrievalEngine
from backend.app.rag.schemas import RetrievalResult
from backend.app.schemas.chat import SourceInfo
from backend.app.services.ai.gemini_client import GeminiClient

logger = get_logger(__name__)

_INJECTION_KEYWORDS: list[str] = [
    "ignore previous instructions",
    "ignore all instructions",
    "ignore your system prompt",
    "repeat your system prompt",
    "act as if",
    "pretend you are",
    "you are now",
    "you are free",
    "override",
    "disregard",
    "forget your",
    "you must obey",
]

_SYSTEM_QUERIES: list[str] = [
    "system prompt",
    "system instructions",
    "what are your instructions",
    "how do you work",
    "tell me your prompt",
    "reveal your",
    "internal instructions",
    "your configuration",
    "your api key",
]

_EMERGENCY_KEYWORDS: list[str] = [
    "severe bleeding",
    "uncontrolled bleeding",
    "facial trauma",
    "broken jaw",
    "swelling affecting breathing",
    "difficulty breathing",
    "trouble swallowing",
    "knocked out tooth",
    "knocked-out tooth",
    "severe pain",
    "dental abscess",
    "swollen face",
    "emergency",
]


class RAGPipeline:
    def __init__(
        self,
        retriever: RetrievalEngine,
        gemini_client: GeminiClient,
        top_k: int = 5,
        max_context_length: int = 4000,
    ) -> None:
        self._retriever = retriever
        self._gemini = gemini_client
        self._top_k = top_k
        self._max_context_length = max_context_length

    def query(
        self,
        user_message: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[str, list[SourceInfo]]:
        message_stripped = user_message.strip()
        if not message_stripped:
            raise ValueError("Message must not be empty.")

        if self._is_injection_attempt(message_stripped):
            logger.warning("Prompt injection attempt detected and blocked.")
            return INJECTION_REFUSAL.strip(), []

        if self._is_system_query(message_stripped):
            logger.info("System information query blocked.")
            return SYSTEM_INFO_REFUSAL.strip(), []

        if self._is_emergency(message_stripped):
            logger.warning("Emergency keywords detected in user message.")

        try:
            results = self._retriever.retrieve(message_stripped, top_k=self._top_k)
        except Exception as exc:
            logger.error(f"Retrieval failed: {exc}")
            raise VectorStoreError("Failed to retrieve relevant information.") from exc

        context, sources = self._build_context(results)
        prompt = self._build_prompt(message_stripped, context, conversation_history or [])

        try:
            answer = self._gemini.generate(prompt)
        except Exception as exc:
            logger.error(f"Gemini generation failed: {exc}")
            raise AIServiceError("The AI service is temporarily unavailable.") from exc

        if not context.strip():
            answer = answer.strip() or NO_CONTEXT_FALLBACK.strip()
            return answer, sources

        return answer.strip(), sources

    def _build_context(
        self,
        results: list[RetrievalResult],
    ) -> tuple[str, list[SourceInfo]]:
        if not results:
            return "", []

        chunks_text: list[str] = []
        source_map: dict[str, SourceInfo] = {}
        total_chars = 0

        for r in results:
            chunk = r.chunk
            snippet = f"[Source: {chunk.filename} / {chunk.heading}]\n{chunk.content}"
            if total_chars + len(snippet) > self._max_context_length:
                break
            chunks_text.append(snippet)
            total_chars += len(snippet)
            key = f"{chunk.filename}:{chunk.chunk_id}"
            if key not in source_map:
                source_map[key] = SourceInfo(
                    filename=chunk.filename,
                    heading=chunk.heading or chunk.subheading or "General",
                    chunk_id=chunk.chunk_id,
                )

        return "\n\n".join(chunks_text), list(source_map.values())

    def _build_prompt(
        self,
        user_message: str,
        context: str,
        history: list[dict[str, str]],
    ) -> str:
        system = SYSTEM_PROMPT.strip()

        if context:
            source_docs = list(
                {s.filename for s in self._extract_sources_from_context(context)}
            )
            context_block = CONTEXT_TEMPLATE.strip().format(
                retrieved_context=context,
                source_documents=", ".join(source_docs) if source_docs else "Knowledge Base",
            )
        else:
            context_block = NO_CONTEXT_FALLBACK.strip()

        prompt_parts = [system, "", "### CONTEXT ###", context_block, ""]

        if history:
            prompt_parts.append("### CONVERSATION HISTORY ###")
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role}: {content}")
            prompt_parts.append("")

        prompt_parts.append("### USER MESSAGE ###")
        prompt_parts.append(f"user: {user_message}")
        prompt_parts.append("")
        prompt_parts.append("### RESPONSE ###")
        prompt_parts.append("assistant:")

        return "\n".join(prompt_parts)

    @staticmethod
    def _extract_sources_from_context(context: str) -> list[SourceInfo]:
        sources: list[SourceInfo] = []
        for line in context.split("\n"):
            if line.startswith("[Source:") and "/" in line:
                parts = line.replace("[Source:", "").replace("]", "").strip()
                if "/" in parts:
                    filename, heading = parts.split("/", 1)
                    sources.append(
                        SourceInfo(
                            filename=filename.strip(),
                            heading=heading.strip(),
                            chunk_id="",
                        )
                    )
        return sources

    @staticmethod
    def _is_injection_attempt(message: str) -> bool:
        msg_lower = message.lower()
        for keyword in _INJECTION_KEYWORDS:
            if keyword in msg_lower:
                return True
        return False

    @staticmethod
    def _is_system_query(message: str) -> bool:
        msg_lower = message.lower()
        for phrase in _SYSTEM_QUERIES:
            if phrase in msg_lower:
                return True
        return False

    @staticmethod
    def _is_emergency(message: str) -> bool:
        msg_lower = message.lower()
        for keyword in _EMERGENCY_KEYWORDS:
            if keyword in msg_lower:
                return True
        return False
