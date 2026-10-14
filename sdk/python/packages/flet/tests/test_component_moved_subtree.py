"""Repro: a component subtree (same outlet object) moved between structurally
different parents (Column <-> Row) must stay mounted and keep reacting."""

import asyncio

import pytest

import flet as ft
from flet.components.component import Component
from flet.controls.context import _context_page
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _Conn(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


async def flush(turns=10):
    for _ in range(turns):
        await asyncio.sleep(0)


def find_components(session, name):
    return [
        c
        for c in session.index.values()
        if isinstance(c, Component) and c.fn.__name__ == name
    ]


def find_texts(session):
    return sorted(c.value for c in session.index.values() if isinstance(c, ft.Text))


H = {}


@ft.component
def Form():
    value, set_value = ft.use_state("loading")
    H["set_form"] = set_value

    def load():
        H.setdefault("loads", 0)
        H["loads"] += 1
        set_value("loaded")

    ft.use_effect(load, [])
    return ft.Text(f"form:{value}")


@ft.component
def PageComp():
    return ft.Container(content=Form())


outlet_ctx = ft.create_context(None)


@ft.component
def Layout():
    mobile, set_mobile = ft.use_state(True)
    H["set_mobile"] = set_mobile
    outlet = ft.use_context(outlet_ctx)
    if mobile:
        return ft.Column(
            controls=[ft.Text("picker"), ft.Container(expand=True, content=outlet)]
        )
    return ft.Row(
        controls=[
            ft.Text("nav"),
            ft.VerticalDivider(width=1),
            ft.Container(expand=True, content=outlet),
        ]
    )


@ft.component
def App():
    return outlet_ctx(PageComp(), lambda: Layout())


@pytest.mark.asyncio
@pytest.mark.parametrize("flips", [1, 2, 3])
async def test_moved_outlet_stays_mounted(flips):
    H.clear()
    conn = _Conn()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    token = _context_page.set(session.page)
    try:
        session.page.render(App)
        session.get_page_patch()
        await flush()
        assert "form:loaded" in find_texts(session)

        for i in range(flips):
            H["set_mobile"](i % 2 == 1)  # True->False->True...
            await flush()

            forms = find_components(session, "Form")
            assert len(forms) == 1, forms
            form = forms[0]
            assert form._state.mounted, f"flip {i}: Form unmounted"
            assert form._state.hooks, f"flip {i}: Form hooks cleared"
            pcs = find_components(session, "PageComp")
            assert len(pcs) == 1 and pcs[0]._state.mounted, f"flip {i}: PageComp"

            # later state update in the moved child must be applied
            H["set_form"](f"updated{i}")
            await flush()
            assert f"form:updated{i}" in find_texts(session), (i, find_texts(session))
    finally:
        session.close()
        await flush()
        _context_page.reset(token)


@pytest.mark.asyncio
async def test_moved_outlet_preserves_state():
    """Stronger: the moved subtree keeps its identity and state (no remount,
    no re-run of mount effects)."""
    H.clear()
    conn = _Conn()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    token = _context_page.set(session.page)
    try:
        session.page.render(App)
        session.get_page_patch()
        await flush()
        form = find_components(session, "Form")[0]
        H["set_form"]("edited")
        await flush()
        for i in range(3):
            H["set_mobile"](i % 2 == 1)
            await flush()
            assert find_components(session, "Form") == [form]
            assert "form:edited" in find_texts(session)
        assert H["loads"] == 1
    finally:
        session.close()
        await flush()
        _context_page.reset(token)
