from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet.controls.page import Page


class Context:
    """
    Manages the context for Flet controls, including page reference
    and auto-update behavior.
    """

    @property
    def page(self) -> "Page":
        """
        Returns the current page associated with the context.

        Returns:
            The current page.

        Raises:
            AssertionError: if property is called outside of Flet app.
        """
        page = _context_page.get()
        assert page, "The context is not associated with any page."
        return page

    def reset_auto_update(self):
        """
        Copies the parent auto-update state into the current context.
        """
        current = _update_behavior_context_var.get()
        new = UpdateBehavior()
        new._auto_update_enabled = current._auto_update_enabled
        _update_behavior_context_var.set(new)

    def enable_auto_update(self):
        """
        Enables auto-update behavior for the current context.
        """
        _update_behavior_context_var.get()._auto_update_enabled = True

    def disable_auto_update(self):
        """
        Disables auto-update behavior for the current context.
        """
        _update_behavior_context_var.get()._auto_update_enabled = False

    def auto_update_enabled(self) -> bool:
        """
        Returns whether auto-update is enabled in the current context.

        Returns:
            `True` if auto-update is enabled, `False` otherwise.
        """
        return _update_behavior_context_var.get()._auto_update_enabled


class UpdateBehavior:
    _auto_update_enabled: bool = True


_context_page = ContextVar("flet_session_page", default=None)

_update_behavior_context_var = ContextVar("update_behavior", default=UpdateBehavior())  # noqa: B039

context = Context()
