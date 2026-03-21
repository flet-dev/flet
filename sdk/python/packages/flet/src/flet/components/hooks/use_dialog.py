from __future__ import annotations

import weakref

from flet.components.hooks.use_effect import use_effect
from flet.components.hooks.use_ref import use_ref
from flet.controls.context import context
from flet.controls.dialog_control import DialogControl


def use_dialog(dialog: DialogControl | None = None):
    """
    Portal a [`DialogControl`][flet.DialogControl] to the page's dialog overlay.

    Call this hook inside a [`@component`][flet.component] function on every render.
    Pass a [`DialogControl`][flet.DialogControl] instance to show the dialog,
    or `None` to hide/remove it. The dialog content is updated
    reactively on each re-render.

    The hook automatically sets `open=True` on the dialog when it is
    added to the overlay and removes it when `None` is passed or the
    component unmounts.

    Args:
        dialog: A [`DialogControl`][flet.DialogControl] to display, or `None`
            to hide it.
    """
    ref = use_ref(None)
    page = context.page

    prev = ref.current

    # Clean up a previously dismissed dialog still in the overlay.
    # Deferred to here (next render) so the dialog stays alive in
    # session.__index (a WeakValueDictionary) long enough for Flutter's
    # dismiss event to reach the Python handler.
    # Do NOT sync __prev_lists here — other hooks may have already
    # appended to _dialogs.controls in this render, and syncing would
    # tell the diff system those additions already happened.  The
    # normal diff will handle the removal correctly.
    if prev is not None and not prev.open and prev in page._dialogs.controls:
        page._dialogs.controls.remove(prev)
        ref.current = None
        prev = None

    if dialog is not None:
        dialog.open = True
        if prev is not None and prev in page._dialogs.controls:
            # Frozen diff: compares prev and dialog field-by-field,
            # sends only actual deltas, and transfers _i via _migrate_state
            # so Flutter preserves widget identity (e.g. TextField cursor).
            page.session.patch_control(control=dialog, prev_control=prev, frozen=True)
            # _dataclass_added (called during frozen diff) skips _parent
            # for the root control when parent=None.  Set it manually so
            # the page property chain works for event dispatch.
            dialog._parent = weakref.ref(page._dialogs)
            # Strip _frozen set by _dataclass_added during frozen diff
            # so we can later set open=False for dismissal.
            if hasattr(dialog, "_frozen"):
                del dialog._frozen
            idx = page._dialogs.controls.index(prev)
            page._dialogs.controls[idx] = dialog
            ref.current = dialog
        else:
            page._dialogs.controls.append(dialog)
            ref.current = dialog
            page.session.schedule_update(page._dialogs)
    elif prev is not None and prev.open:
        # Dismiss: patch open=False so Flutter pops the dialog route.
        # Keep prev in _dialogs.controls and ref.current so the dialog
        # stays alive in session.__index (WeakValueDictionary) — Flutter
        # needs the control present to dispatch the dismiss event.
        # Cleanup happens on the next render (above).
        prev.open = False
        page.session.patch_control(prev)

    def _cleanup():
        d = ref.current
        if d is not None:
            if d.open:
                d.open = False
                page.session.patch_control(d)
            if d in page._dialogs.controls:
                page._dialogs.controls.remove(d)
                page.session.schedule_update(page._dialogs)
            ref.current = None

    use_effect(lambda: None, dependencies=[], cleanup=_cleanup)
