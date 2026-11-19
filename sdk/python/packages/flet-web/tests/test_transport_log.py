"""Tests for the debug logging of messages in `FletApp`'s transport."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import msgpack
import pytest
import pytest_asyncio

from flet.messaging.protocol import Message, MessageAction
from flet_web.fastapi.flet_app import FletApp

pytestmark = pytest.mark.asyncio


class CountingBody(dict):
    """A message body that counts how many times it is turned into text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reprs = 0

    def __repr__(self):
        self.reprs += 1
        return super().__repr__()


@pytest_asyncio.fixture
async def app():
    """A `FletApp` with a send queue and a stub session, not connected to a
    client."""
    with ThreadPoolExecutor() as executor:
        app = FletApp(asyncio.get_running_loop(), executor, None, None)
        app._FletApp__send_queue = asyncio.Queue()
        app._FletApp__session = Mock()
        yield app


class TestSendMessage:
    """Logging of messages sent to the client."""

    async def test_not_turned_into_text_without_debug(self, app, caplog):
        """With debug logging off, a sent message is not turned into text."""
        body = CountingBody(id=1, patch=[0, 0])

        with caplog.at_level(logging.INFO, logger="flet_transport"):
            app.send_message(Message(MessageAction.PATCH_CONTROL, body))

        assert body.reprs == 0
        assert caplog.records == []

    async def test_logged_with_debug(self, app, caplog):
        """With debug logging on, a sent message is logged."""
        body = CountingBody(id=1, patch=[0, 0])

        with caplog.at_level(logging.DEBUG, logger="flet_transport"):
            app.send_message(Message(MessageAction.PATCH_CONTROL, body))

        assert "send_message:" in caplog.text
        assert "'patch': [0, 0]" in caplog.text

    @pytest.mark.parametrize("level", [logging.INFO, logging.DEBUG])
    async def test_sent_unchanged(self, app, caplog, level):
        """The message is sent the same way whether debug logging is on or off."""
        with caplog.at_level(level, logger="flet_transport"):
            app.send_message(
                Message(MessageAction.PATCH_CONTROL, {"id": 1, "patch": [0, 0]})
            )

        packet = app._FletApp__send_queue.get_nowait()
        assert packet[0] == 0x00
        assert msgpack.unpackb(packet[1:]) == [
            MessageAction.PATCH_CONTROL.value,
            {"id": 1, "patch": [0, 0]},
        ]


class TestReceivedMessage:
    """Logging of messages received from the client."""

    async def test_not_turned_into_text_without_debug(self, app, caplog):
        """With debug logging off, a received message is not turned into text."""
        body = CountingBody(id=1, props={"value": "a"})

        with caplog.at_level(logging.INFO, logger="flet_transport"):
            await app._FletApp__on_message(
                [MessageAction.UPDATE_CONTROL_PROPS.value, body]
            )

        assert body.reprs == 0
        assert caplog.records == []
        app._FletApp__session.apply_patch.assert_called_once_with(1, {"value": "a"})

    async def test_logged_with_debug(self, app, caplog):
        """With debug logging on, a received message is logged."""
        body = CountingBody(id=1, props={"value": "a"})

        with caplog.at_level(logging.DEBUG, logger="flet_transport"):
            await app._FletApp__on_message(
                [MessageAction.UPDATE_CONTROL_PROPS.value, body]
            )

        assert "_on_message:" in caplog.text
        assert "'value': 'a'" in caplog.text
