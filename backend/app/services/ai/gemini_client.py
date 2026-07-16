from __future__ import annotations

from typing import Final

import google.generativeai as genai

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class GeminiClient:
    _SAFETY_DEFAULTS: Final[list[dict[str, str]]] = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-1.5-flash",
        max_output_tokens: int = 1024,
        temperature: float = 0.3,
    ) -> None:
        if not api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY in your .env file."
            )

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "max_output_tokens": max_output_tokens,
                "temperature": temperature,
            },
            safety_settings=self._SAFETY_DEFAULTS,
        )
        self._model_name = model_name
        logger.info(f"Gemini client initialized (model={model_name})")

    def generate(self, prompt: str) -> str:
        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as exc:
            logger.error(f"Gemini API call failed: {exc}")
            raise
