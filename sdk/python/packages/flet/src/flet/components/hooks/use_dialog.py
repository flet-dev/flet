from __future__ import annotations

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

    if prev is not None and prev not in page._dialogs.controls:
        ref.current = None
        prev = None

    if dialog is not None:
        dialog.open = True
        page._prepare_dialog(dialog)
        if prev is not None and prev in page._dialogs.controls:
            # Frozen diff: compares prev and dialog field-by-field,
            # sends only actual deltas, and transfers _i via _migrate_state
            # so Flutter preserves widget identity (e.g. TextField cursor).
            page.session.patch_control(control=dialog, prev_control=prev, frozen=True)
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
        # needs the control present to dispatch the dismiss event. The
        # wrapped dismiss handler removes it after Flutter signals close.
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
