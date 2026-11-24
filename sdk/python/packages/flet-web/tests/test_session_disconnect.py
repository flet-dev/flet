"""A client that disconnects while `main` runs doesn't fail the session."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import pytest

from flet.messaging.session import Session
from flet_web.fastapi.flet_app import FletApp
from flet_web.fastapi.flet_app_manager import app_manager


@pytest.mark.asyncio
async def test_main_finishes_after_the_client_disconnects(caplog):
    released = asyncio.Event()
    finished = []

    async def main(page):
        await released.wait()
        finished.append(page)

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        app = FletApp(loop, executor, main, None)
        app.pubsubhub = app_manager.get_pubsubhub(main, loop=loop)
        session = Session(app)
        # What REGISTER_CLIENT does for a new session, before starting `main`.
        app._FletApp__session = session
        task = asyncio.create_task(app._FletApp__on_session_created())
        await asyncio.sleep(0)

        # The browser reloads while `main` waits: the server disconnects the
        # session, which disposes this connection.
        await session.disconnect(60)
        released.set()
        with caplog.at_level(logging.ERROR, logger="flet_web.fastapi"):
            await task

    assert finished == [session.page]
    assert "Unhandled error" not in caplog.text
