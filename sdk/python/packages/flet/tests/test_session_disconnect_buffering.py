import asyncio
from datetime import datetime, timezone

import pytest

from flet.components.component import Component
from flet.components.hooks.use_effect import EffectHook
from flet.messaging.connection import Connection
from flet.messaging.protocol import Message, MessageAction, SessionCrashedBody
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
        Message(MessageAction.SESSION_CRASHED, SessionCrashedBody("x"))
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

    buffered_message = Message(
        MessageAction.SESSION_CRASHED, SessionCrashedBody("buffered")
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


@pytest.mark.asyncio
async def test_cleanup_returned_by_effect_setup_runs_on_unmount():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    component = Component(fn=lambda: None, args=(), kwargs={})
    component._state.mounted = True
    cleanup_ran = asyncio.Event()

    def cleanup():
        cleanup_ran.set()

    hook = EffectHook(component, setup=lambda: None, _returned_cleanup=cleanup)
    component._state.hooks = [hook]
    component._schedule_effect = session.schedule_effect  # type: ignore[method-assign]
    component._run_unmount_effects()
    session.start_updates_scheduler()

    await asyncio.wait_for(cleanup_ran.wait(), timeout=1)
    session._Session__closed = True
    session._Session__updates_ready.set()
    await session._Session__updates_task


@pytest.mark.asyncio
async def test_unmount_cancels_pending_async_effect_setup():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    component = Component(fn=lambda: None, args=(), kwargs={})
    component._state.mounted = True
    started = asyncio.Event()

    async def setup():
        started.set()
        await asyncio.Event().wait()

    task = asyncio.create_task(setup())
    await started.wait()
    hook = EffectHook(component, setup=setup)
    hook._setup_task = task
    component._state.hooks = [hook]
    component._schedule_effect = session.schedule_effect  # type: ignore[method-assign]
    component._run_unmount_effects()
    session.start_updates_scheduler()

    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(task, timeout=1)
    session._Session__closed = True
    session._Session__updates_ready.set()
    await session._Session__updates_task
