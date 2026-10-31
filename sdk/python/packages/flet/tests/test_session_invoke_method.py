import asyncio

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.messages = []

    def send_message(self, message):
        # Real transports serialize each patch before the next diff is computed.
        msgpack.packb(message, default=configure_encode_object_for_msgpack(BaseControl))
        self.messages.append(message)


def _session():
    conn = _RecordingConnection()
    return Session(conn), conn


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [None, "Timeout waiting for invoke method listener"])
async def test_reply_after_control_removal_resolves_call_and_keeps_session_usable(
    error,
):
    session, conn = _session()
    field = ft.TextField()
    session.page.controls.append(field)
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(BaseControl),
    )
    assert field._i in session.index

    call = asyncio.create_task(session.invoke_method(field._i, "focus", {}))
    await asyncio.sleep(0)
    call_id = conn.messages[-1].body.call_id

    session.page.controls.clear()
    session.page.update()
    assert field._i not in session.index

    session.handle_invoke_method_results(field._i, call_id, "value", error)

    if error:
        with pytest.raises(RuntimeError, match=error):
            await asyncio.wait_for(call, timeout=1)
    else:
        assert await asyncio.wait_for(call, timeout=1) == "value"

    # A late reply must not prevent subsequent calls from completing.
    next_call = asyncio.create_task(
        session.invoke_method(session.page._i, "get_value", {})
    )
    await asyncio.sleep(0)
    next_call_id = conn.messages[-1].body.call_id
    session.handle_invoke_method_results(
        session.page._i, next_call_id, "next value", None
    )
    assert await asyncio.wait_for(next_call, timeout=1) == "next value"


def test_reply_for_removed_control_without_pending_call_is_ignored():
    session, _ = _session()

    session.handle_invoke_method_results(987654321, "unknown-call", None, None)


@pytest.mark.asyncio
async def test_reply_for_registered_control_returns_the_result():
    session, conn = _session()
    page_id = session.page._i

    call = asyncio.create_task(session.invoke_method(page_id, "get_value", {}))
    await asyncio.sleep(0)
    call_id = conn.messages[-1].body.call_id

    session.handle_invoke_method_results(page_id, call_id, "value", None)

    assert await asyncio.wait_for(call, timeout=1) == "value"
