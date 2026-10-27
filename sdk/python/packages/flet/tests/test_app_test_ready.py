import asyncio
import importlib

import msgpack
import pytest

import flet as ft
from flet.messaging.connection import Connection
from flet.messaging.protocol import MessageAction, configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

_on_session_created = importlib.import_module("flet.app").__get_on_session_created


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.messages = []

    def send_message(self, message):
        self.messages.append(
            msgpack.packb(
                [message.action, message.body],
                default=configure_encode_object_for_msgpack(ft.BaseControl),
            )
        )


def _session(test=True):
    conn = _RecordingConnection()
    session = Session(conn)
    session.page.test = test
    # Match registration: snapshot the page before main() runs.
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(ft.BaseControl),
    )
    return session, conn


@pytest.mark.asyncio
async def test_readiness_follows_delayed_main_and_its_ui_updates():
    session, conn = _session()
    started = asyncio.Event()
    release = asyncio.Event()

    async def main(page):
        page.add(ft.Text("Loading"))
        started.set()
        await release.wait()
        page.controls = [ft.Text("Ready")]
        page.update()

    task = asyncio.create_task(_on_session_created(main)(session))
    try:
        await started.wait()
        assert not session.page._internals.get("test_ready")
        assert conn.messages
        assert all(b"test_ready" not in m for m in conn.messages)
    finally:
        release.set()
        await task

    assert session.page._internals["test_ready"] is True
    assert b"Ready" in conn.messages[-2]
    assert b"test_ready" in conn.messages[-1]


@pytest.mark.asyncio
@pytest.mark.parametrize("test", [True, False])
async def test_empty_main_is_ready_only_in_test_mode(test):
    session, conn = _session(test=test)
    await _on_session_created(lambda page: None)(session)

    assert bool(session.page._internals.get("test_ready")) is test
    assert any(b"test_ready" in m for m in conn.messages) is test


@pytest.mark.asyncio
async def test_main_failure_reports_error_without_readiness():
    session, conn = _session()

    async def main(page):
        raise RuntimeError("Initialization failed")

    await _on_session_created(main)(session)

    assert not session.page._internals.get("test_ready")
    action, body = msgpack.unpackb(conn.messages[-1], strict_map_key=False)
    assert action == MessageAction.SESSION_CRASHED.value
    assert "Initialization failed" in body["message"]


@pytest.mark.asyncio
@pytest.mark.parametrize("async_generator", [True, False])
async def test_generator_main_is_ready_after_first_yield(async_generator):
    session, conn = _session()
    ready_during_iteration = []

    async def async_main(page):
        page.controls.append(ft.Text("Ready"))
        yield
        ready_during_iteration.append(page._internals.get("test_ready"))
        yield

    def sync_main(page):
        page.controls.append(ft.Text("Ready"))
        yield
        ready_during_iteration.append(page._internals.get("test_ready"))
        yield

    await _on_session_created(async_main if async_generator else sync_main)(session)

    assert ready_during_iteration == [True]
    assert sum(b"test_ready" in m for m in conn.messages) == 1
