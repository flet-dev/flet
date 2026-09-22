from contextvars import ContextVar
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet.controls.page import Page


class Context:
    """
    Manages the context for Flet controls, including page reference and auto-update \
    behavior.

    Context instance is accessed via :data:`flet.context`.
    """

    def __init__(self) -> None:
        pass

    def __current_session(self):
        """Return the Session bound to the current context, or None.

        Components mode is tracked per-session rather than on this global
        singleton so that multiple concurrently running apps in one process
        (e.g. an embedded `FletApp` inside a host app) don't clobber each
        other's mode. Resolved via the same page context var used by
        :attr:`page`.
        """
        page = _context_page.get()
        if page is None:
            return None
        try:
            return page.session
        except RuntimeError:
            return None

    def __update_behavior(self) -> "UpdateBehavior":
        """Return the `UpdateBehavior` writes and reads should act on.

        Falls back to the process-wide default when the current context has
        none of its own - which is the case at module scope, before any app
        session has started.
        """
        return _update_behavior_context_var.get() or _app_update_behavior

    @property
    def page(self) -> "Page":
        """
        Returns the current :class:`~flet.Page` associated with the context.

        Example:
            ```python
            # take page width anywhere in the app
            width = ft.context.page.width
            ```

        Returns:
            The current page.

        Raises:
            RuntimeError: If the property is accessed outside a running Flet app.
        """
        page = _context_page.get()
        if page is None:
            raise RuntimeError(
                "The context is not associated with any page. "
                "Make sure you are accessing ft.context.page "
                "inside a Flet app callback."
            )
        return page

    def enable_auto_update(self):
        """
        Enables auto-update behavior for the current context.

        Example:
            ```python
            import flet as ft

            # disable auto-update globally for the app
            ft.context.disable_auto_update()


            def main(page: ft.Page):
                # enable auto-update just inside main
                ft.context.enable_auto_update()

                page.controls.append(ft.Text("Hello, world!"))
                # page.update() - we don't need to call it explicitly


            ft.run(main)
            ```
        """
        self.__update_behavior()._auto_update_enabled = True

    def disable_auto_update(self):
        """
        Disables auto-update behavior for the current context.

        Example:
            ```python
            import flet as ft


            def main(page: ft.Page):
                def button_click():
                    ft.context.disable_auto_update()
                    b.content = "Button clicked!"
                    # update just the button
                    b.update()

                    page.controls.append(ft.Text("This won't appear"))
                    # no page.update() will be called here

                page.controls.append(b := ft.Button("Action!", on_click=button_click))
                # page.update() - auto-update is enabled by default


            ft.run(main)
        ```
        """
        self.__update_behavior()._auto_update_enabled = False

    def enable_components_mode(self):
        """
        Enables components mode in the current context.
        """
        if (session := self.__current_session()) is not None:
            session.components_mode = True

    def disable_components_mode(self):
        """
        Disables components mode in the current context.
        """
        if (session := self.__current_session()) is not None:
            session.components_mode = False

    def is_components_mode(self) -> bool:
        """
        Returns whether the current context is in components mode.

        Returns:
            `True` if in components mode, `False` otherwise.
        """
        session = self.__current_session()
        return session.components_mode if session is not None else False

    def mark_update_called(self):
        """
        Marks that `.update()` was explicitly called during the current handler.
        """
        self.__update_behavior()._update_called = True

    def was_update_called(self) -> bool:
        """
        Returns whether `.update()` was explicitly called during the current handler.

        Returns:
            `True` if `.update()` was called, `False` otherwise.
        """
        return self.__update_behavior()._update_called

    def reset_update_called(self):
        """
        Resets the update-called flag for the current context.
        """
        self.__update_behavior()._update_called = False

    def auto_update_enabled(self) -> bool:
        """
        Returns whether auto-update is enabled in the current context.

        Returns:
            `True` if auto-update is enabled, `False` otherwise.
        """
        return (
            not self.is_components_mode()
            and self.__update_behavior()._auto_update_enabled
        )

    def reset_auto_update(self):
        """
        Starts a fresh auto-update state for the current context.

        The new state inherits the enclosing context's auto-update setting, or
        the app-wide default when the context has none of its own - which is
        the case for a session starting up, or for an event handler, since each
        event is dispatched in its own task.

        The `_update_called` flag is deliberately not inherited: it records
        whether `.update()` was called during *this* handler.
        """
        new = UpdateBehavior()
        new._auto_update_enabled = self.__update_behavior()._auto_update_enabled
        _update_behavior_context_var.set(new)


class UpdateBehavior:
    """
    Internal class used by the Context API to manage auto-update behavior.

    An instance of UpdateBehavior is stored in a context variable and tracks
    whether automatic updates are enabled for the current context. The Context
    class interacts with UpdateBehavior to enable, disable, and query the
    auto-update state.
    """

    _auto_update_enabled: bool = True
    _update_called: bool = False


_context_page = ContextVar("flet_session_page", default=None)

_app_update_behavior = UpdateBehavior()
"""
Process-wide default `UpdateBehavior`.

Calling `ft.context.disable_auto_update()` at module scope - a documented way to
turn auto-update off for a whole app - happens before any session exists, so
there is no context to write to. Those calls land here, and every context-scoped
`UpdateBehavior` is rooted at this value.

This is deliberately a separate object from the `_update_behavior_context_var`
default: when the ContextVar itself defaulted to a shared mutable instance, a
contextless call mutated the very object every unrelated context observed, so
one app could silently turn auto-update off for every other app in the process.
"""

_update_behavior_context_var: ContextVar[Optional[UpdateBehavior]] = ContextVar(
    "update_behavior", default=None
)
"""
Context-scoped `UpdateBehavior`, or `None` to fall back to `_app_update_behavior`.

The `None` default is what keeps contextless calls from mutating state that
other contexts can see - see `_app_update_behavior`.
"""

context = Context()
"""Global context object for the running Flet app.

Use :data:`flet.context` to access the current page and control
auto-update behavior inside callbacks.
"""
