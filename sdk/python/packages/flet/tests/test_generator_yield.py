"""Tests for the updates sent at each `yield` of a generator handler or `main()`.

A `yield` asks for an intermediate UI update, but the patch it produces is only
*queued* on the connection's send queue. The generator therefore has to give the
event loop a turn before it resumes - otherwise blocking work placed right after
the `yield` (the classic `time.sleep()`) holds the queued patch back until the
whole generator returns.
"""

import asyncio
import importlib
import time

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.core.text import Text
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

_on_session_created = importlib.import_module("flet.app").__get_on_session_created

# Long enough that a missing yield is unambiguous, short enough to stay cheap.
BLOCK_SECONDS = 0.05


class QueueingConnection(Connection):
    """Connection that queues outbound messages, like the socket transport.

    `FletSocketServer.send_message` packs the message and does a `put_nowait`
    onto an `asyncio.Queue` drained by a background send loop, so nothing
    reaches the client until the event loop gets a turn.
    """

    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.queue: asyncio.Queue = asyncio.Queue()

    def send_message(self, message):
        # Packing is what refreshes the diff snapshots the next patch is
        # calculated against, so it has to happen here, as in the real
        # transports - not in the send loop.
        self.queue.put_nowait(
            msgpack.packb(
                [message.action, message.body],
                default=configure_encode_object_for_msgpack(BaseControl),
            )
        )


async def _send_loop(conn: QueueingConnection, log: list[str]):
    """Stand-in for the transport's send loop: records every flushed message."""
    while True:
        await conn.queue.get()
        log.append("sent")


def _new_session(conn: QueueingConnection, *controls: BaseControl) -> Session:
    """A session showing `controls`, bootstrapped as `REGISTER_CLIENT` would."""
    session = Session(conn)
    session.page.controls.extend(controls)
    # Mounts the tree into the session index and seeds the diff snapshots.
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(BaseControl),
    )
    return session


async def _dispatch_tap(text: Text, log: list[str]):
    """Tap `text` with a send loop running, appending to the ordered log."""
    conn = QueueingConnection()
    session = _new_session(conn, text)
    loop_task = asyncio.create_task(_send_loop(conn, log))
    try:
        await session.dispatch_event(text._i, "tap", None)
        await asyncio.sleep(0)  # let the send loop drain the trailing patch
    finally:
        loop_task.cancel()


async def _start_session(main, log: list[str]):
    """Run `main` as a new session does, with a send loop recording to `log`."""
    conn = QueueingConnection()
    session = _new_session(conn)
    loop_task = asyncio.create_task(_send_loop(conn, log))
    try:
        await _on_session_created(main)(session)
        await asyncio.sleep(0)  # let the send loop drain the trailing patch
    finally:
        loop_task.cancel()


class TestGeneratorHandlerYield:
    """A `yield` in an event handler sends pending updates before it resumes."""

    @pytest.mark.asyncio
    async def test_sync_generator_handler_flushes_patch_at_yield(self):
        """A sync generator handler sends its update before blocking work."""
        log: list[str] = []
        text = Text("start")

        def handler(e):
            text.value = "step 1"
            yield
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)
            text.value = "step 2"

        text.on_tap = handler
        await _dispatch_tap(text, log)

        assert log == ["sent", "blocked", "sent"]

    @pytest.mark.asyncio
    async def test_async_generator_handler_flushes_patch_at_yield(self):
        """An async generator handler sends its update before blocking work."""
        log: list[str] = []
        text = Text("start")

        async def handler(e):
            text.value = "step 1"
            yield
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)
            text.value = "step 2"

        text.on_tap = handler
        await _dispatch_tap(text, log)

        assert log == ["sent", "blocked", "sent"]

    @pytest.mark.asyncio
    async def test_explicit_update_in_generator_handler_is_flushed_at_yield(self):
        """The yield must also cover handlers that update controls themselves.

        An explicit `.update()` suppresses the post-event auto-update, so a fix
        hung off auto-update alone would leave this path blocked.
        """
        log: list[str] = []
        text = Text("start")

        def handler(e):
            text.value = "step 1"
            text.update()
            yield
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)
            text.value = "step 2"

        text.on_tap = handler
        await _dispatch_tap(text, log)

        assert log == ["sent", "blocked", "sent"]

    @pytest.mark.asyncio
    async def test_plain_handler_does_not_yield_mid_dispatch(self):
        """Non-generator handlers keep running to completion without interleaving.

        The yield belongs to the generator boundary only - a plain handler must not
        gain a new suspension point in the middle of dispatch.
        """
        log: list[str] = []
        text = Text("start")

        def handler(e):
            text.value = "step 1"
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)

        text.on_tap = handler
        await _dispatch_tap(text, log)

        assert log == ["blocked", "sent"]


class TestGeneratorMainYield:
    """A `yield` in `main()` sends pending updates before `main()` resumes."""

    @pytest.mark.asyncio
    async def test_sync_generator_main_flushes_patch_at_yield(self):
        """A sync generator `main()` sends its update before blocking work."""
        log: list[str] = []

        def main(page: ft.Page):
            page.add(ft.Text("Loading..."))
            yield
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)
            page.add(ft.Text("Ready"))

        await _start_session(main, log)

        assert log == ["sent", "blocked", "sent"]

    @pytest.mark.asyncio
    async def test_async_generator_main_flushes_patch_at_yield(self):
        """An async generator `main()` sends its update before blocking work."""
        log: list[str] = []

        async def main(page: ft.Page):
            page.add(ft.Text("Loading..."))
            yield
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)
            page.add(ft.Text("Ready"))

        await _start_session(main, log)

        assert log == ["sent", "blocked", "sent"]

    @pytest.mark.asyncio
    async def test_plain_main_does_not_yield_mid_run(self):
        """A plain `main()` runs to completion before its updates are sent."""
        log: list[str] = []

        def main(page: ft.Page):
            page.add(ft.Text("Loading..."))
            log.append("blocked")
            time.sleep(BLOCK_SECONDS)
            page.add(ft.Text("Ready"))

        await _start_session(main, log)

        # One patch per `page.add()`, both sent after `main()` returns.
        assert log == ["blocked", "sent", "sent"]
