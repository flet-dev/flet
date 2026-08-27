"""Generator event handlers must yield to the event loop at every `yield`.

A `yield` in an event handler is an explicit request for an intermediate UI
update, but the patch it produces is only *queued* on the connection's send
queue. The handler therefore has to give the event loop a turn before it
resumes - otherwise blocking work placed right after the `yield` (the classic
`time.sleep()`) holds the queued patch back until the whole handler returns.
"""

import asyncio
import time

import msgpack
import pytest

from flet.controls.base_control import BaseControl
from flet.controls.core.text import Text
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

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


def _mounted_session(text: Text) -> tuple[Session, QueueingConnection]:
    """A session showing `text`, bootstrapped as `REGISTER_CLIENT` would."""
    conn = QueueingConnection()
    session = Session(conn)
    session.page.controls.append(text)
    # Mounts the tree into the session index and seeds the diff snapshots.
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(BaseControl),
    )
    return session, conn


async def _dispatch_tap(text: Text, log: list[str]):
    """Tap `text` with a send loop running, appending to the ordered log."""
    session, conn = _mounted_session(text)
    loop_task = asyncio.create_task(_send_loop(conn, log))
    try:
        await session.dispatch_event(text._i, "tap", None)
        await asyncio.sleep(0)  # let the send loop drain the trailing patch
    finally:
        loop_task.cancel()


@pytest.mark.asyncio
async def test_sync_generator_handler_flushes_patch_at_yield():
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
async def test_async_generator_handler_flushes_patch_at_yield():
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
async def test_explicit_update_in_generator_handler_is_flushed_at_yield():
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
async def test_plain_handler_does_not_yield_mid_dispatch():
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
