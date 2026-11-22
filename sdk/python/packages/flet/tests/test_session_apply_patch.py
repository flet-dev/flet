"""
`Session.apply_patch()` applies props sent by the client (`UPDATE_CONTROL_PROPS`).
The client must not be able to set server-only fields: `skip` fields like `data`,
private `_` names and event handlers.
"""

import logging

import flet as ft
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


def _create_session() -> Session:
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    return Session(conn)


def _index(session: Session, control):
    session.index[control._i] = control
    return control


def test_client_cannot_overwrite_page_data():
    session = _create_session()
    page = session.page
    page.data = {"user": "alice", "groups": ["operators"]}

    session.apply_patch(page._i, {"data": {"user": "alice", "groups": ["admins"]}})

    assert page.data == {"user": "alice", "groups": ["operators"]}


def test_client_cannot_overwrite_control_data():
    session = _create_session()
    field = _index(session, ft.TextField(data="server"))

    session.apply_patch(field._i, {"data": "client"})

    assert field.data == "server"


def test_client_cannot_write_private_names():
    session = _create_session()
    field = _index(session, ft.TextField())

    session.apply_patch(field._i, {"_private": "x", "_i": 999})

    assert not hasattr(field, "_private")
    assert field._i != 999


def test_client_cannot_write_event_handlers():
    session = _create_session()

    def handler(e):
        pass

    field = _index(session, ft.TextField(on_change=handler))

    session.apply_patch(field._i, {"on_change": "x"})

    assert field.on_change is handler


def test_client_can_write_regular_props():
    session = _create_session()
    field = _index(session, ft.TextField(value="old"))

    session.apply_patch(field._i, {"value": "new"})

    assert field.value == "new"


def test_page_patch_still_applies_client_props():
    session = _create_session()

    session.apply_page_patch({"route": "/settings", "width": 800})

    assert session.page.route == "/settings"
    assert session.page.width == 800


def test_client_can_report_autocomplete_selected_index():
    session = _create_session()
    auto = _index(session, ft.AutoComplete(suggestions=[]))

    session.apply_patch(auto._i, {"_selected_index": 2})

    assert auto.selected_index == 2


def test_client_can_report_dismissed_snack_bar():
    session = _create_session()
    snack = _index(session, ft.SnackBar(ft.Text("hi")))

    session.apply_patch(snack._i, {"_dismissed": True})

    assert snack._dismissed is True


def test_ignored_keys_are_logged(caplog):
    session = _create_session()
    field = _index(session, ft.TextField())

    with caplog.at_level(logging.WARNING, logger="flet"):
        session.apply_patch(field._i, {"data": 1, "value": "ok"})

    assert "TextField.data" in caplog.text
    assert "TextField.value" not in caplog.text
