"""An embedded app asks its host with `page.request_host()`; the host answers in
`FletApp.on_guest_request`."""

import asyncio

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


def _pack(value):
    return msgpack.packb(
        value, default=configure_encode_object_for_msgpack(BaseControl)
    )


class _Connection(Connection):
    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()

    def send_message(self, message):
        _pack([message.action, message.body])


_sessions = []  # parents are weak references: keep each test's session alive


async def _host(app: ft.FletApp, monkeypatch) -> list:
    """Shows `app` on a host page; returns the list its replies go to."""
    session = Session(_Connection())
    _sessions.append(session)
    session.connection.loop = asyncio.get_running_loop()
    session.page.controls.append(app)
    _pack(session.get_page_patch())
    replies = []

    async def invoke(self, method_name, arguments=None, timeout=None):
        _pack(arguments)  # unsendable replies fail here, as in a real transport
        replies.append((method_name, arguments))

    monkeypatch.setattr(ft.FletApp, "_invoke_method", invoke)
    return replies


async def _ask(app, replies, request="share", args=None, request_id=7):
    await app.page.session.dispatch_event(
        app._i,
        "guest_request",
        {"request_id": request_id, "request": request, "args": args},
    )
    for _ in range(100):
        if replies:
            break
        await asyncio.sleep(0.01)
    assert len(replies) == 1
    name, arguments = replies.pop()
    assert name == "reply_guest_request"
    assert arguments["request_id"] == request_id
    return {k: v for k, v in arguments.items() if k != "request_id"}


@pytest.mark.asyncio
async def test_handler_result_is_the_reply(monkeypatch):
    seen = []

    async def on_request(e: ft.FletAppGuestRequestEvent):
        seen.append((e.request, e.args, e.control))
        await asyncio.sleep(0)
        return {"shared": True}

    app = ft.FletApp(url="", on_guest_request=on_request)
    replies = await _host(app, monkeypatch)
    assert await _ask(app, replies, args={"title": "Notes"}) == {
        "result": {"shared": True}
    }
    assert seen == [("share", {"title": "Notes"}, app)]


@pytest.mark.asyncio
async def test_sync_handler_and_none_result(monkeypatch):
    app = ft.FletApp(url="", on_guest_request=lambda e: None)
    replies = await _host(app, monkeypatch)
    assert await _ask(app, replies) == {"result": None}


@pytest.mark.asyncio
async def test_unhandled_refused_and_failed(monkeypatch):
    def on_request(e: ft.FletAppGuestRequestEvent):
        if e.request == "share":
            return ft.HostRequest.UNHANDLED
        if e.request == "ask":
            raise ft.HostRequestRefused("The user said no.")
        raise ValueError("boom")

    app = ft.FletApp(url="", on_guest_request=on_request)
    replies = await _host(app, monkeypatch)
    assert (await _ask(app, replies, "share"))["error"]["kind"] == "unhandled"
    assert await _ask(app, replies, "ask") == {
        "error": {"kind": "refused", "message": "The user said no."}
    }
    assert await _ask(app, replies, "other") == {
        "error": {"kind": "failed", "message": "boom"}
    }


@pytest.mark.asyncio
async def test_unsendable_result_fails_the_request(monkeypatch):
    app = ft.FletApp(url="", on_guest_request=lambda e: object())
    replies = await _host(app, monkeypatch)
    assert (await _ask(app, replies))["error"]["kind"] == "failed"


@pytest.mark.asyncio
async def test_slow_handler_does_not_hold_up_other_events(monkeypatch):
    release = asyncio.Event()
    titles = []

    async def on_request(e):
        await release.wait()
        return "done"

    app = ft.FletApp(
        url="",
        on_guest_request=on_request,
        on_title_change=lambda e: titles.append(e.data),
    )
    replies = await _host(app, monkeypatch)
    session = app.page.session
    await session.dispatch_event(
        app._i, "guest_request", {"request_id": 1, "request": "slow", "args": None}
    )
    # The request is still waiting, yet the next event is handled.
    await session.dispatch_event(app._i, "title_change", "Hi")
    assert titles == ["Hi"]
    assert replies == []
    release.set()
    for _ in range(100):
        if replies:
            break
        await asyncio.sleep(0.01)
    assert replies == [("reply_guest_request", {"request_id": 1, "result": "done"})]


@pytest.mark.asyncio
async def test_request_host_returns_result_and_raises_errors(monkeypatch):
    calls = []
    answers = [
        {"result": {"fb_code": "c"}},
        {"error": {"kind": "refused", "message": "No"}},
    ]

    async def invoke(self, method_name, arguments=None, timeout=None):
        calls.append((method_name, arguments, timeout))
        return answers.pop(0)

    monkeypatch.setattr(ft.Page, "_invoke_method", invoke)
    session = Session(_Connection())
    page = session.page
    page.embedded = True

    assert await page.request_host("fletbase.oauth", {"provider": "x"}, 30) == {
        "fb_code": "c"
    }
    assert calls == [
        (
            "request_host",
            {"name": "fletbase.oauth", "args": {"provider": "x"}, "timeout_ms": 30000},
            35,
        )
    ]
    with pytest.raises(ft.HostRequestError) as info:
        await page.request_host("fletbase.oauth")
    assert (info.value.kind, info.value.message) == ("refused", "No")
    assert calls[1][1]["timeout_ms"] is None and calls[1][2] is None


@pytest.mark.asyncio
async def test_request_host_outside_an_embedded_app(monkeypatch):
    session = Session(_Connection())
    page = session.page
    with pytest.raises(ft.HostRequestError) as info:
        await page.request_host("share")
    assert info.value.kind == "not_embedded"


@pytest.mark.asyncio
async def test_reply_after_the_host_went_away_is_dropped(monkeypatch):
    app = ft.FletApp(url="", on_guest_request=lambda e: "late")
    await _host(app, monkeypatch)

    async def gone(self, method_name, arguments=None, timeout=None):
        raise RuntimeError("Session closed")

    monkeypatch.setattr(ft.FletApp, "_invoke_method", gone)
    event = ft.FletAppGuestRequestEvent(
        control=app, name="guest_request", request="x", request_id=3
    )
    await app._answer_guest_request(event)  # doesn't raise
