"""Tests that a connection registers with a session once."""

import msgpack
from fastapi.testclient import TestClient

import flet_web.fastapi as flet_fastapi


def _frame(action, body) -> bytes:
    return b"\x00" + msgpack.packb([action, body])


def _register(route: str) -> bytes:
    return _frame(1, {"session_id": "", "page_name": "", "page": {"route": route}})


def test_repeated_registration_is_ignored():
    """A second registration on a connection changes nothing and fires no event."""
    events = []
    routes = []

    async def main(page):
        routes.append(page.route)
        page.on_connect = lambda e: events.append("connect")
        page.on_route_change = lambda e: events.append("route_change")

    with (
        TestClient(flet_fastapi.app(main)) as client,
        client.websocket_connect("/ws") as socket,
    ):
        socket.send_bytes(_register("/first"))
        socket.receive_bytes()
        socket.send_bytes(_register("/second"))
        socket.send_bytes(b"\xff")

    assert routes == ["/first"]
    assert events == []
