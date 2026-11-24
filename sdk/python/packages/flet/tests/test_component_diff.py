"""Regression tests for ObjectPatch diff behaviour around Component reconciliation."""

import asyncio
import gc
import weakref

import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.controls.object_patch import ObjectPatch
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


@ft.component
def _CompA():
    return ft.Text("a")


@ft.component
def _CompB():
    return ft.Text("b")


def _make_container(component_fn):
    """Build Container(content=component_fn()) in a fresh renderer context."""
    from flet.components.component import Renderer

    with Renderer().with_context():
        return ft.Container(content=component_fn())


def test_diff_replaces_incompatible_component_in_scalar_field():
    """Changing `Container.content` from one Component fn to another must
    produce a remove + add (not an in-place migrate), so the new component
    receives a fresh `_i` and `did_mount` is fired.

    Regression: before this fix, `_compare_values` called
    `_compare_dataclasses` on both Components because `type(src) is
    type(dst) == Component`.  `_migrate_state` then copied `_i` from
    the old instance to the new one, so the session's add/remove dedup logic
    considered the new component already mounted and silently skipped
    `did_mount` (and thus `use_effect` mount setup).
    """
    old_root = _make_container(_CompA)
    new_root = _make_container(_CompB)

    old_content_i = old_root.content._i
    new_content_i_before = new_root.content._i

    _patch, added_controls, removed_controls = ObjectPatch.from_diff(
        old_root, new_root, control_cls=BaseControl, frozen=True
    )

    added_ids = {c._i for c in added_controls}
    removed_ids = {c._i for c in removed_controls}

    # The new Component must be mounted (in added_controls) AND the old
    # Component must be unmounted (in removed_controls) — under distinct ids
    # so the session's session.py dedup logic does not cancel the did_mount.
    assert new_root.content._i == new_content_i_before, (
        "Incompatible Components must NOT migrate _i"
    )
    assert old_content_i in removed_ids, (
        f"old component _i={old_content_i} must be in removed {removed_ids}"
    )
    assert new_root.content._i in added_ids, (
        f"new component _i={new_root.content._i} must be in added {added_ids}"
    )
    assert new_root.content._i != old_content_i


def test_diff_migrates_same_component_fn_when_args_differ():
    """Sanity check: Components with the same `fn` but different args (so
    they don't compare equal) must still migrate `_i` in place, so hook
    state survives a re-render.
    """
    from flet.components.component import Renderer

    @ft.component
    def _Comp(label: str):
        return ft.Text(label)

    with Renderer().with_context():
        old_root = ft.Container(content=_Comp("one"))
    with Renderer().with_context():
        new_root = ft.Container(content=_Comp("two"))

    old_content_i = old_root.content._i

    ObjectPatch.from_diff(old_root, new_root, control_cls=BaseControl, frozen=True)

    # Migration: same fn → _i copied from old to new.
    assert new_root.content._i == old_content_i


def test_diff_key_change_on_scalar_field_forces_remount():
    """A `key` change on a single-child dataclass field (e.g.
    `Container.content`) must force a remove + add, the same way list
    reconciliation does for keyed list items. Without this, patterns like
    `ft.Container(content=ft.FletApp(key=str(reload_key)))` silently
    ignore key changes — the Control's `key` property flips on Dart but
    the Flutter Element/State is kept, so the widget never actually
    remounts.
    """
    from flet.components.component import Renderer

    with Renderer().with_context():
        old_root = ft.Container(content=ft.Text("hello", key="0"))
    with Renderer().with_context():
        new_root = ft.Container(content=ft.Text("hello", key="1"))

    old_content_i = old_root.content._i
    new_content_i_before = new_root.content._i

    _patch, added_controls, removed_controls = ObjectPatch.from_diff(
        old_root, new_root, control_cls=BaseControl, frozen=True
    )

    added_ids = {c._i for c in added_controls}
    removed_ids = {c._i for c in removed_controls}

    # Different key → old Text must be unmounted, new Text mounted with its
    # own (not migrated) _i.
    assert new_root.content._i == new_content_i_before, (
        "Keyed child must NOT migrate _i from the old instance"
    )
    assert old_content_i in removed_ids
    assert new_root.content._i in added_ids
    assert new_root.content._i != old_content_i


def test_diff_same_key_on_scalar_field_reconciles_in_place():
    """Sanity check: when the `key` matches across renders, the child is
    reconciled in place (same as no key at all).
    """
    from flet.components.component import Renderer

    with Renderer().with_context():
        old_root = ft.Container(content=ft.Text("first", key="same"))
    with Renderer().with_context():
        new_root = ft.Container(content=ft.Text("second", key="same"))

    old_content_i = old_root.content._i

    ObjectPatch.from_diff(old_root, new_root, control_cls=BaseControl, frozen=True)

    assert new_root.content._i == old_content_i


@pytest.mark.asyncio
@pytest.mark.parametrize("key", [None, "child"])
@pytest.mark.parametrize("sibling_mode", ["none", "insert", "remove"])
async def test_component_passed_as_control_prop_survives_wrapper_updates(
    key, sibling_mode
):
    """A retained child must keep its client IDs, events, and independent state."""
    from flet.components.component import Renderer

    clicks = []
    setters = {}
    renders = []

    @ft.component
    def Child():
        count, set_count = ft.use_state(0)
        setters["child"] = set_count
        renders.append(count)
        return ft.Container(
            content=ft.Text(str(count)),
            on_click=lambda e: clicks.append("child"),
        )

    @ft.component
    def Wrapper(controls):
        count, set_count = ft.use_state(0)
        setters["wrapper"] = set_count
        show_sibling = (sibling_mode == "insert" and count % 2 == 1) or (
            sibling_mode == "remove" and count % 2 == 0
        )
        siblings = [ft.Text("Sibling", key="sibling")] if show_sibling else []
        return ft.Column([ft.Text(str(count)), *siblings, *controls])

    conn = Connection()
    conn.pubsubhub = PubSubHub()
    conn.send_message = lambda message: None
    session = Session(conn)
    token = _context_page.set(session.page)
    try:
        with Renderer().with_context():
            child = Child(key=key)
            direct = ft.Button("Direct", on_click=lambda e: clicks.append("direct"))
            wrapper = Wrapper([direct, child])
        session.page.render(lambda: wrapper)
        session.get_page_patch()
        clickable_ref = weakref.ref(child._b)
        client_id = child._b._i

        for count in (1, 2):
            setters["wrapper"](count)
            for _ in range(5):
                await asyncio.sleep(0)
            gc.collect()

            # Event dispatch can repair stale parent links, so check them first.
            assert child.parent is wrapper._b
            assert child.page is session.page
            assert direct.parent is wrapper._b
            assert direct.page is session.page

            await session.dispatch_event(client_id, "click", None)
            await session.dispatch_event(direct._i, "click", None)
            assert clicks == ["child", "direct"] * count
            assert child._b is clickable_ref()
            assert session.index[client_id] is child._b
            assert child.parent is wrapper._b
            assert child.page is session.page
            assert not child._stale
            assert renders == [0]

        setters["child"](1)
        for _ in range(5):
            await asyncio.sleep(0)
        assert child._b.content.value == "1"
        assert child._b._i == client_id
        assert renders == [0, 1]
    finally:
        session.close()
        for _ in range(5):
            await asyncio.sleep(0)
        _context_page.reset(token)
