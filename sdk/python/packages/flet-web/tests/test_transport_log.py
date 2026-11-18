"""Transport debug logging doesn't format messages while debug logging is off."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import pytest

from flet.messaging.protocol import Message, MessageAction
from flet_web.fastapi.flet_app import FletApp


class CountingBody(dict):
    """Message body that counts how many times it's turned into text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reprs = 0

    def __repr__(self):
        self.reprs += 1
        return super().__repr__()


async def send(caplog, level):
    """Sends a message with debug logging at `level` and returns its body and the
    sent packet."""

    body = CountingBody(id=1, patch=[0, 0])

    with ThreadPoolExecutor() as executor:
        app = FletApp(asyncio.get_running_loop(), executor, None, None)
        app._FletApp__send_queue = asyncio.Queue()

        with caplog.at_level(level, logger="flet_transport"):
            app.send_message(Message(MessageAction.PATCH_CONTROL, body))

        return body, app._FletApp__send_queue.get_nowait()


@pytest.mark.asyncio
async def test_send_message_skips_formatting_without_debug(caplog):
    # A big page patch takes minutes and gigabytes to turn into text, so it must
    # only happen when someone reads the debug log.
    body, packet = await send(caplog, logging.INFO)

    assert body.reprs == 0
    assert packet.startswith(b"\x00")
    assert "send_message" not in caplog.text


@pytest.mark.asyncio
async def test_send_message_logs_with_debug(caplog):
    body, packet = await send(caplog, logging.DEBUG)

    assert body.reprs > 0
    assert packet.startswith(b"\x00")
    assert "send_message: Message(action=<MessageAction.PATCH_CONTROL" in caplog.text
