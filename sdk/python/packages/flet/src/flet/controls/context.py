from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet.controls.page import Page


class Context:
    """
    Manages the context for Flet controls, including page reference
    and auto-update behavior.

    Context instance is accessed via [`flet.context`][flet.context].
    """

    def __init__(self) -> None:
        self.__components_mode = False

    @property
    def page(self) -> "Page":
        """
        Returns the current [`Page`][flet.] associated with the context.

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
        _update_behavior_context_var.get()._auto_update_enabled = True

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
        _update_behavior_context_var.get()._auto_update_enabled = False

    def enable_components_mode(self):
        """
        Enables components mode in the current context.
        """
        self.__components_mode = True

    def is_components_mode(self) -> bool:
        """
        Returns whether the current context is in components mode.

        Returns:
            `True` if in components mode, `False` otherwise.
        """
        return self.__components_mode

    def auto_update_enabled(self) -> bool:
        """
        Returns whether auto-update is enabled in the current context.

        Returns:
            `True` if auto-update is enabled, `False` otherwise.
        """
        return (
            not self.__components_mode
            and _update_behavior_context_var.get()._auto_update_enabled
        )

    def reset_auto_update(self):
        """
        Copies the parent auto-update state into the current context.
        """
        current = _update_behavior_context_var.get()
        new = UpdateBehavior()
        new._auto_update_enabled = current._auto_update_enabled
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


_context_page = ContextVar("flet_session_page", default=None)

_update_behavior_context_var = ContextVar("update_behavior", default=UpdateBehavior())  # noqa: B039

context = Context()
