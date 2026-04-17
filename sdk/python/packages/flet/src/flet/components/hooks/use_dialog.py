from __future__ import annotations

import dataclasses
import weakref

from flet.components.hooks.use_effect import use_effect
from flet.components.hooks.use_ref import use_ref
from flet.controls.context import context
from flet.controls.dialog_control import DialogControl


def _find_dialog_index(dialogs, target):
    # Identity (`is`) comparison — dialog controls are dataclasses and two
    # dialogs built from the same field values compare equal with `==`,
    # so `in` / `.index()` would match the wrong entry when two sibling
    # hosts each manage a similarly-shaped dialog.
    for i, c in enumerate(dialogs.controls):
        if c is target:
            return i
    return -1


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


def _sync_open_dialog(page, prev: DialogControl, dialog: DialogControl) -> bool:
    """
    Copy the latest rendered dialog fields onto the mounted dialog instance.

    Keeping `prev` alive preserves its `_i`, `_parent`, wrapped dismiss handler,
    and the Flutter widget state (including the live route that was pushed by
    `showDialog`). The fresh `dialog` instance is treated as render-time input
    only and discarded after its state is copied over.
    """

    dialog.open = True
    ui_changed = False

    for field in dataclasses.fields(dialog):
        name = field.name

        if name.startswith("_") or name == "open":
            continue

        if field.metadata.get("skip", False):
            if name == "data" and prev.data != dialog.data:
                prev.data = dialog.data
            continue

        if name == "on_dismiss":
            continue

        next_value = getattr(dialog, name)
        if getattr(prev, name) == next_value:
            continue

        setattr(prev, name, next_value)
        ui_changed = True

    if not prev.open:
        prev.open = True
        ui_changed = True

    if prev.parent is not page._dialogs:
        page._set_dialog_parent(prev)

    _bind_dialog_subtree(prev, page._dialogs)

    if page._get_original_dialog_on_dismiss(prev) is not dialog.on_dismiss:
        prev.on_dismiss = dialog.on_dismiss
        page._wrap_dialog_on_dismiss(prev)

    return ui_changed


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
        if (
            prev is not None
            and prev_idx >= 0
            and prev.open
            and type(prev) is type(dialog)
        ):
            # Preserve the mounted dialog instance so Flutter keeps the same
            # route/state object, but refresh its latest render-time fields so
            # props and closures remain live while the dialog stays open.
            # Queue the patch through the normal scheduler so component
            # reconciliation finishes before dialog children are reindexed.
            if _sync_open_dialog(page, prev, dialog):
                page.session.schedule_update(prev)
            ref.current = prev
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
        # Dismiss: flip open=False and coalesce the patch through the
        # parent `_dialogs` control.  An immediate `patch_control(prev)`
        # here would race with a sibling host's `schedule_update(_dialogs)`
        # — both patches land on Flutter in separate messages and the
        # overlay rebuild can disrupt an in-flight dismiss animation.
        # Routing both dismiss and show paths through `_dialogs.update()`
        # emits a single batched patch per scheduler tick.
        prev.open = False
        page.session.schedule_update(page._dialogs)

    def _cleanup():
        d = ref.current
        if d is not None:
            ref.current = None
            if d.open:
                d.open = False
                page.session.schedule_update(page._dialogs)

    use_effect(lambda: None, dependencies=[], cleanup=_cleanup)
