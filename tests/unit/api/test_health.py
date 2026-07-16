from backend.app.api.v1.endpoints.health import START_TIME
from backend.app.core.config import settings


def test_health_endpoint_exists():
    from backend.app.api.v1.endpoints.health import router
    assert router is not None


def test_start_time_set():
    assert START_TIME > 0


def test_settings_loaded():
    assert settings.app_name == "Rashid Dental AI Assistant"
    assert settings.app_version == "1.0.0"
    assert settings.api_v1_prefix == "/api/v1"
