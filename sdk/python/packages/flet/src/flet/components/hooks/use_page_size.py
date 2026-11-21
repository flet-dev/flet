from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar, overload

from flet.components.hooks.use_effect import use_effect
from flet.components.hooks.use_ref import use_ref
from flet.components.hooks.use_state import use_state
from flet.controls.context import context
from flet.controls.geometry import Size

__all__ = ["use_page_size"]

SelectedT = TypeVar("SelectedT")


def _page_size(page: Any) -> Size:
    return Size(page.width or 0, page.height or 0)


@overload
def use_page_size() -> Size: ...


@overload
def use_page_size(select: Callable[[Size], SelectedT]) -> SelectedT: ...


def use_page_size(select: Callable[[Size], Any] | None = None) -> Any:
    """
    Read the page size and re-render the component when it changes.

    Call it inside a :func:`~flet.component` function. Without arguments it
    returns the page's :class:`~flet.Size` and re-renders the component on every
    resize. With `select`, it returns `select(size)` and re-renders only when
    that value changes, so a layout that only depends on a breakpoint re-renders
    only when the page crosses it.

    Unlike :attr:`~flet.Page.on_resize`, which holds one handler, any number of
    components can use this hook at once.

    Args:
        select: A function that maps the page size to the value the component
            needs, such as `lambda size: size.width < 600`.

    Returns:
        The page size, or `select(size)` when `select` is given.

    Example:
        ```python
        @ft.component
        def Shell(body: ft.Control):
            compact = ft.use_page_size(lambda size: size.width < 600)
            if compact:
                return ft.Column([body, NavBar()], expand=True)
            return ft.Row([NavRail(), body], expand=True)
        ```
    """
    page = context.page
    select_ref = use_ref()
    select_ref.current = select

    def selected(size: Size) -> Any:
        fn = select_ref.current
        return fn(size) if fn is not None else size

    size_ref = use_ref(lambda: _page_size(page))
    _, set_selected = use_state(lambda: selected(size_ref.current))

    def subscribe():
        def on_resize(size: Size):
            size_ref.current = size
            set_selected(selected(size))

        # Catch up with a resize between the first render and this effect.
        on_resize(_page_size(page))
        return page._add_resize_listener(on_resize)

    use_effect(subscribe, [])

    return selected(size_ref.current)
