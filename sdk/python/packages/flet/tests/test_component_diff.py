"""Regression tests for ObjectPatch diff behaviour around Component reconciliation."""

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.object_patch import ObjectPatch


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
    """Changing ``Container.content`` from one Component fn to another must
    produce a remove + add (not an in-place migrate), so the new component
    receives a fresh ``_i`` and ``did_mount`` is fired.

    Regression: before this fix, ``_compare_values`` called
    ``_compare_dataclasses`` on both Components because ``type(src) is
    type(dst) == Component``.  ``_migrate_state`` then copied ``_i`` from
    the old instance to the new one, so the session's add/remove dedup logic
    considered the new component already mounted and silently skipped
    ``did_mount`` (and thus ``use_effect`` mount setup).
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
    """Sanity check: Components with the same ``fn`` but different args (so
    they don't compare equal) must still migrate ``_i`` in place, so hook
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
