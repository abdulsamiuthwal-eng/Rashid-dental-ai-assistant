import pytest
from backend.app.schemas.chat import ChatRequest, ChatResponse, SourceInfo


def test_chat_request_valid():
    req = ChatRequest(message="Hello", session_id="session-1")
    assert req.message == "Hello"
    assert req.session_id == "session-1"


def test_chat_request_empty_message_raises():
    with pytest.raises(ValueError):
        ChatRequest(message="", session_id=None)


def test_chat_request_whitespace_only_raises():
    with pytest.raises(ValueError):
        ChatRequest(message="   ", session_id=None)


def test_chat_request_without_session():
    req = ChatRequest(message="Hello")
    assert req.session_id is None


def test_chat_response_with_sources():
    sources = [
        SourceInfo(filename="services.md", heading="General Dentistry", chunk_id="s1"),
        SourceInfo(filename="pricing.md", heading="Consultation", chunk_id="s2"),
    ]
    resp = ChatResponse(message="Here is the info.", session_id="sid-1", sources=sources)
    assert len(resp.sources) == 2
    assert resp.sources[0].filename == "services.md"
    assert resp.sources[1].heading == "Consultation"


def test_chat_response_empty_sources():
    resp = ChatResponse(message="No info found.", session_id="sid-1", sources=[])
    assert resp.sources == []


def test_source_info_fields():
    source = SourceInfo(filename="test.md", heading="Test Heading", chunk_id="test_0_abc")
    assert source.filename == "test.md"
    assert source.heading == "Test Heading"
    assert source.chunk_id == "test_0_abc"
