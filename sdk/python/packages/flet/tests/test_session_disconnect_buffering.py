from datetime import datetime, timezone

from flet.components.component import Component
from flet.components.hooks.use_effect import EffectHook
from flet.messaging.connection import Connection
from flet.messaging.protocol import ClientAction, ClientMessage, SessionCrashedBody
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


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
