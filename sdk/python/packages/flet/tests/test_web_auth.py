"""WebAuth Service — TDD."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import msgpack
import pytest

from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.web_auth import WebAuth
from flet.controls.types import PagePlatform
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    configure_encode_object_for_msgpack,
    decode_ext_from_msgpack,
)
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


def _wire(obj: Any) -> Any:
    packed = msgpack.packb(
        obj, default=configure_encode_object_for_msgpack(BaseControl)
    )
    return msgpack.unpackb(
        packed, ext_hook=decode_ext_from_msgpack, strict_map_key=False
    )


class _Conn(Connection):
    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.page_name = "/"
        self.messages = []

    def send_message(self, message):
        _wire([message.action, message.body])
        self.messages.append(message)


@pytest.fixture
def mobile_session():
    s = Session(_Conn())
    _wire(s.get_page_patch())
    s.page.web = False
    s.page.platform = PagePlatform.ANDROID
    token = _context_page.set(s.page)
    yield s
    _context_page.reset(token)


@pytest.mark.asyncio
async def test_start_requires_callback_scheme_on_mobile(mobile_session):
    web_auth = WebAuth()
    with pytest.raises(ValueError, match="callback_scheme"):
        await web_auth.start()


@pytest.mark.asyncio
async def test_start_sets_redirect_url_from_scheme(mobile_session):
    web_auth = WebAuth()
    session = await web_auth.start(callback_scheme="com.example.app.auth")
    assert session.redirect_url == "com.example.app.auth://callback"


@pytest.mark.asyncio
async def test_authenticate_returns_callback_url(mobile_session):
    web_auth = WebAuth()
    web_auth._invoke_method = AsyncMock(  # type: ignore[method-assign]
        return_value={
            "callback_url": "com.example.app.auth://callback?code=abc&state=xyz"
        }
    )
    session = await web_auth.start(callback_scheme="com.example.app.auth")
    callback = await session.authenticate(
        "https://idp.example/authorize?...", ephemeral=True
    )
    assert "code=abc" in callback
    assert "state=xyz" in callback
    call = web_auth._invoke_method.await_args
    assert call.args[0] == "authenticate"
    assert call.args[1]["ephemeral"] is True
    assert call.args[1]["redirect_url"] == "com.example.app.auth://callback"


@pytest.mark.asyncio
async def test_unsupported_on_web():
    s = Session(_Conn())
    _wire(s.get_page_patch())
    s.page.web = True
    token = _context_page.set(s.page)
    try:
        web_auth = WebAuth()
        with pytest.raises(FletUnsupportedPlatformException):
            await web_auth.start(callback_scheme="com.example.app.auth")
    finally:
        _context_page.reset(token)
