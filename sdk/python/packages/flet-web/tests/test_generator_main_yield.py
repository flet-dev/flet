"""A `yield` in `main()` sends pending updates before `main()` resumes.

`FletApp.send_message` only queues the patch; the WebSocket send loop, a task
on the same event loop, sends it. `main()` therefore has to give the loop a
turn at each `yield`, or blocking work right after it holds the patch back.
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet_web.fastapi.flet_app import FletApp
from flet_web.fastapi.flet_app_manager import app_manager

# Long enough that a missing yield is unambiguous, short enough to stay cheap.
BLOCK_SECONDS = 0.05


async def _start_session(main, log: list[str]):
    """Run `main` as `FletApp` does for a new session, recording sends to `log`."""
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        app = FletApp(loop, executor, main, None)
        app.pubsubhub = app_manager.get_pubsubhub(main, loop=loop)
        send_queue: asyncio.Queue = asyncio.Queue()
        app._FletApp__send_queue = send_queue
        session = Session(app)
        # What REGISTER_CLIENT does for a new session, before starting `main`:
        # mount the page and seed the diff snapshots.
        msgpack.packb(
            session.get_page_patch(),
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        app._FletApp__session = session

        async def send_loop():
            # Stand-in for `FletApp.__send_loop`, which needs a WebSocket.
            while True:
                await send_queue.get()
                log.append("sent")

        send_loop_task = asyncio.create_task(send_loop())
        try:
            await app._FletApp__on_session_created()
            await asyncio.sleep(0)  # let the send loop drain the trailing patch
        finally:
            send_loop_task.cancel()


@pytest.mark.asyncio
async def test_sync_generator_main_flushes_patch_at_yield():
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
async def test_async_generator_main_flushes_patch_at_yield():
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
async def test_plain_main_does_not_yield_mid_run():
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
