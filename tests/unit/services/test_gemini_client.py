import pytest
from backend.app.services.ai.gemini_client import GeminiClient


def test_init_raises_on_empty_api_key():
    with pytest.raises(ValueError, match="Gemini API key is required"):
        GeminiClient(api_key="")


def test_init_with_api_key():
    client = GeminiClient(api_key="fake-key")
    assert client is not None
    assert client._model_name == "gemini-1.5-flash"


def test_init_with_custom_model():
    client = GeminiClient(api_key="fake-key", model_name="gemini-1.5-pro")
    assert client._model_name == "gemini-1.5-pro"


def test_init_with_custom_temperature():
    client = GeminiClient(api_key="fake-key", temperature=0.7)
    assert client is not None
