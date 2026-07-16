from backend.app.core.config import Settings


def test_default_settings():
    settings = Settings()
    assert settings.app_name == "Rashid Dental AI Assistant"
    assert settings.app_version == "1.0.0"
    assert settings.gemini_model == "gemini-1.5-flash"
    assert settings.rag_top_k == 5
    assert settings.conversation_memory_window == 10


def test_api_prefix():
    settings = Settings()
    assert settings.api_v1_prefix == "/api/v1"


def test_is_development_default():
    settings = Settings()
    assert settings.is_development is True


def test_is_production_false_by_default():
    settings = Settings()
    assert settings.is_production is False
