from __future__ import annotations

import dataclasses
import weakref

from flet.components.hooks.use_effect import use_effect
from flet.components.hooks.use_ref import use_ref
from flet.controls.context import context
from flet.controls.dialog_control import DialogControl


def _index_of(controls, target):
    # Identity (`is`) comparison — dialog controls are dataclasses and two
    # dialogs built from the same field values compare equal with `==`,
    # so `in` / `.index()` would match the wrong entry when two sibling
    # hosts each manage a similarly-shaped dialog.
    for i, c in enumerate(controls):
        if c is target:
            return i
    return -1


def _find_dialog_index(dialogs, target):
    return _index_of(dialogs.controls, target)


def _dialogs_snapshot(dialogs):
    """`_dialogs.controls` as the client last saw it.

    Returns `None` when `_dialogs` has never been serialized or diffed, i.e.
    there is no client-side view to keep in sync yet.
    """
    prev_lists = getattr(dialogs, "__prev_lists", None)
    return prev_lists.get("controls") if prev_lists is not None else None


def _bind_dialog_subtree(value, parent):
    if dataclasses.is_dataclass(value):
        if parent is not None and parent is not value:
            value._parent = weakref.ref(parent)
        for field in dataclasses.fields(value):
            if not field.metadata.get("skip", False):
                _bind_dialog_subtree(getattr(value, field.name), value)
    elif isinstance(value, list):
        for item in value:
            _bind_dialog_subtree(item, parent)
    elif isinstance(value, dict):
        for item in value.values():
            _bind_dialog_subtree(item, parent)


def use_dialog(dialog: DialogControl | None = None):
    """
    Portal a :class:`~flet.DialogControl` to the page's dialog overlay.

    Call this hook inside a :func:`~flet.component` function on every render.
    Pass a :class:`~flet.DialogControl` instance to show the dialog,
    or `None` to hide/remove it.

    The hook automatically sets `open=True` on the dialog when it is
    added to the overlay and removes it when `None` is passed or the
    component unmounts.

    Args:
        dialog: A :class:`~flet.DialogControl` to display, or `None`
            to hide it.
    """
    ref = use_ref(None)
    page = context.page

    prev = ref.current

    if prev is not None and _find_dialog_index(page._dialogs, prev) < 0:
        ref.current = None
        prev = None

    if dialog is not None:
        prev_idx = _find_dialog_index(page._dialogs, prev) if prev is not None else -1
        snapshot = _dialogs_snapshot(page._dialogs)
        # Where `prev` sits in the client's view of the list. This is NOT
        # `prev_idx`: the live list can have entries appended or removed since
        # the last flush, so the two indices drift apart. `-1` with a snapshot
        # present means the client has never seen `prev` — it was appended by
        # an earlier render in this same scheduler batch and the queued
        # `_dialogs` update hasn't been flushed yet.
        snapshot_idx = (
            _index_of(snapshot, prev)
            if snapshot is not None and prev is not None
            else -1
        )
        if (
            prev is not None
            and prev_idx >= 0
            and prev.open
            and type(prev) is type(dialog)
        ):
            dialog.open = True
            page._prepare_dialog(dialog)
            if snapshot is None or snapshot_idx >= 0:
                # Frozen diff: compares prev and dialog field-by-field,
                # migrates `_i` onto the new instance via `_migrate_state`,
                # and emits only actual field deltas. This is what preserves
                # Flutter widget identity for nested controls — notably the
                # TextField inside an AlertDialog keeps its cursor/focus
                # across re-renders.
                page.session.patch_control(
                    control=dialog, prev_control=prev, frozen=True
                )
                # Strip the `_frozen` marker set by _dataclass_added during
                # the frozen diff so we can later set open=False for dismissal.
                if hasattr(dialog, "_frozen"):
                    del dialog._frozen
            # Replace the old instance with the new one in the overlay list
            # — at the SAME index, so sibling hosts' entries aren't disturbed.
            _bind_dialog_subtree(dialog, page._dialogs)
            page._dialogs.controls[prev_idx] = dialog
            if snapshot_idx >= 0:
                # Keep `_dialogs.__prev_lists['controls']` aligned with the new
                # instance. Without this, a later `_dialogs.update()` triggered
                # by an unrelated operation (e.g. `page.show_dialog(SnackBar)`)
                # would diff the fresh `controls` list against a snapshot
                # pointing at the old Python object — different `id()`, so the
                # diff emits a full REPLACE of the dialog. On Dart, REPLACE
                # creates a new Control with `_open` unset, and the next build
                # re-enters the show branch and pushes a second DialogRoute on
                # top of the existing one. The dialog then refuses to close.
                snapshot[snapshot_idx] = dialog
            elif snapshot is not None:
                # `prev` never reached the client, so there is nothing to
                # patch against — a PATCH_CONTROL for its `_i` would be
                # dropped client-side as an out-of-sync control. The queued
                # `_dialogs` update carries the fresh instance instead;
                # re-arm it in case it was already drained this batch.
                page.session.schedule_update(page._dialogs)
            ref.current = dialog
        else:
            dialog.open = True
            page._prepare_dialog(dialog)
            _bind_dialog_subtree(dialog, page._dialogs)
            # Either `prev` is gone (already dismissed on the client) or
            # is still in the list with `open=False` (mid-dismiss,
            # awaiting the client's on_dismiss round-trip).  In the
            # latter case we must NOT reuse `prev`'s `_i` — Flutter's
            # `AlertDialogControl` still carries `_open=True` locally
            # from when the previous dialog was shown, so reusing `_i`
            # means the new `open=True` patch hits `open == lastOpen`
            # and the new dialog never calls `showDialog`.  Append a
            # fresh entry (new `_i`) and let the dismissing one finish
            # on its own.
            page._dialogs.controls.append(dialog)
            ref.current = dialog
            page.session.schedule_update(page._dialogs)
    elif prev is not None and prev.open:
        # Dismiss: flip open=False and patch the dialog directly.  The
        # frozen-patch path above swaps the dialog instance in
        # `_dialogs.controls`, which desyncs `_dialogs.__prev_lists`
        # — so a `schedule_update(_dialogs)` here would miss the
        # `open=False` delta entirely. Patching `prev` directly is both
        # cheaper (one op vs a full list diff) and unaffected by the
        # list-snapshot state.
        prev.open = False
        page.session.patch_control(prev)

    def _cleanup():
        d = ref.current
        if d is not None:
            ref.current = None
            if d.open:
                d.open = False
                page.session.patch_control(d)

    use_effect(lambda: None, dependencies=[], cleanup=_cleanup)
