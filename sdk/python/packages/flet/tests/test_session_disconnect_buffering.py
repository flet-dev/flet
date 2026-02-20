from datetime import datetime, timezone

from flet.components.component import Component
from flet.components.hooks.use_effect import EffectHook
from flet.messaging.connection import Connection
from flet.messaging.protocol import ClientAction, ClientMessage, SessionCrashedBody
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


def test_disconnected_session_drops_incremental_messages():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    session._Session__conn = None
    session._Session__expires_at = datetime.now(timezone.utc)

    session._Session__send_message(  # type: ignore[attr-defined]
        ClientMessage(ClientAction.SESSION_CRASHED, SessionCrashedBody("x"))
    )

    assert session._Session__send_buffer == []


def test_disconnected_session_ignores_scheduled_updates_and_effects():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    session._Session__conn = None
    session._Session__expires_at = datetime.now(timezone.utc)

    session.schedule_update(session.page)
    hook = EffectHook(
        Component(fn=lambda: None, args=(), kwargs={}),
        setup=lambda: None,
    )
    session.schedule_effect(hook, is_cleanup=False)

    assert len(session._Session__pending_updates) == 0
    assert len(session._Session__pending_effects) == 0


def test_attach_connection_restores_state_and_flushes_buffer():
    initial_conn = Connection()
    initial_conn.pubsubhub = PubSubHub()
    session = Session(initial_conn)

    buffered_message = ClientMessage(
        ClientAction.SESSION_CRASHED, SessionCrashedBody("buffered")
    )
    session._Session__conn = None
    session._Session__expires_at = datetime.now(timezone.utc)
    session._Session__send_buffer = [buffered_message]

    new_conn = _RecordingConnection()
    new_conn.pubsubhub = PubSubHub()

    session.attach_connection(new_conn)

    assert session.connection is new_conn
    assert session.expires_at is None
    assert session._Session__send_buffer == []
    assert new_conn.messages == [buffered_message]
