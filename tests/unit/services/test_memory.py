from backend.app.services.ai.memory import ConversationMemory


def test_get_or_create_session_returns_new_session():
    memory = ConversationMemory()
    sid = memory.get_or_create_session()
    assert sid is not None
    assert len(sid) > 0


def test_get_or_create_session_reuses_existing():
    memory = ConversationMemory()
    sid = memory.get_or_create_session("test-session")
    assert sid == "test-session"


def test_add_and_get_history():
    memory = ConversationMemory(window_size=5)
    sid = memory.get_or_create_session("test-session")
    memory.add_message(sid, "user", "Hello")
    memory.add_message(sid, "assistant", "Hi there")
    history = memory.get_history(sid)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there"


def test_window_size_respected():
    memory = ConversationMemory(window_size=3)
    sid = memory.get_or_create_session("test-session")
    for i in range(10):
        memory.add_message(sid, "user", f"msg{i}")
        memory.add_message(sid, "assistant", f"resp{i}")
    history = memory.get_history(sid)
    assert len(history) == 3


def test_empty_session_returns_empty_list():
    memory = ConversationMemory()
    assert memory.get_history("nonexistent") == []


def test_multiple_sessions_isolated():
    memory = ConversationMemory()
    sid1 = memory.get_or_create_session("session-1")
    sid2 = memory.get_or_create_session("session-2")
    memory.add_message(sid1, "user", "Hello from 1")
    memory.add_message(sid2, "user", "Hello from 2")
    assert len(memory.get_history(sid1)) == 1
    assert len(memory.get_history(sid2)) == 1


def test_session_id_generated_when_none():
    memory = ConversationMemory()
    sid1 = memory.get_or_create_session()
    sid2 = memory.get_or_create_session()
    assert sid1 != sid2


def test_stale_session_eviction():
    memory = ConversationMemory(window_size=10, session_ttl=0)
    sid = memory.get_or_create_session("stale-session")
    memory.add_message(sid, "user", "test")
    import time
    time.sleep(0.1)
    history = memory.get_history(sid)
    assert len(history) == 0
