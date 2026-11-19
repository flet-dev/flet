"""Tests for intermediate UI updates from a generator `main()`.

A `yield` in `main()` asks for an intermediate update, such as a splash
screen shown before slow startup work. The patch it produces is only queued
on the connection's send queue, so it reaches the client only once `main()`
gives the event loop a turn.
"""

import asyncio
import time

import msgpack
import pytest

import flet as ft
from flet.app import __get_on_session_created as get_on_session_created
from flet.controls.base_control import BaseControl
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session

from .test_generator_handler_yield import QueueingConnection, _send_loop

# Long enough that a missing yield is unambiguous, short enough to stay cheap.
BLOCK_SECONDS = 0.05


async def _start_session(main, log: list[str]):
    """Run `main` as a new session would, with a send loop recording to `log`."""
    session = Session(QueueingConnection())
    # Seeds the diff snapshots, as `REGISTER_CLIENT` does.
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(BaseControl),
    )
    loop_task = asyncio.create_task(_send_loop(session.connection, log))
    try:
        await get_on_session_created(main)(session)
        await asyncio.sleep(0)  # let the send loop drain the trailing patch
    finally:
        loop_task.cancel()


class TestGeneratorMainYield:
    """A `yield` in `main()` sends pending updates before `main()` resumes."""

    @pytest.mark.asyncio
    async def test_sync_generator_main_flushes_patch_at_yield(self):
        """A sync generator `main()` sends its splash before blocking work."""
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
        """An async generator `main()` sends its splash before blocking work."""
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

        assert log[0] == "blocked"
