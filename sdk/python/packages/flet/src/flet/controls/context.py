from contextvars import ContextVar
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet.controls.page import Page


class Context:
    @property
    def page(self) -> Optional["Page"]:
        return _context_page.get()

    def reset_auto_update(self):
        """Copies parent state into current context."""
        current = _update_behavior_context_var.get()
        new = UpdateBehavior()
        new._auto_update_enabled = current._auto_update_enabled
        _update_behavior_context_var.set(new)

    def enable_auto_update(self):
        _update_behavior_context_var.get()._auto_update_enabled = True

    def disable_auto_update(self):
        _update_behavior_context_var.get()._auto_update_enabled = False

    def auto_update_enabled(self):
        return _update_behavior_context_var.get()._auto_update_enabled


class UpdateBehavior:
    _auto_update_enabled: bool = True


_context_page = ContextVar("flet_session_page", default=None)

_update_behavior_context_var = ContextVar("update_behavior", default=UpdateBehavior())  # noqa: B039

context = Context()
