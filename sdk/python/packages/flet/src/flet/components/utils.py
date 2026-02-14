import contextvars
import math
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flet.components.component import Component, Renderer


_CURRENT_RENDERER: "contextvars.ContextVar[Renderer | None]" = contextvars.ContextVar(
    "CURRENT_RENDERER", default=None
)


def current_renderer() -> "Renderer":
    """
    Returns the renderer bound to the current execution context.

    The active renderer is stored in a context variable and is set while running
    inside `Renderer.render(...)` or `Renderer.with_context(...)`.

    Returns:
        The current [`Renderer`][flet.Renderer].

    Raises:
        RuntimeError: If no renderer is currently bound.
    """
    r = _CURRENT_RENDERER.get()
    if r is None:
        raise RuntimeError(
            "No current renderer is set. Call via Renderer.render(...) "
            "or Renderer.with_context(...)."
        )
    return r


def current_component() -> "Component":
    """
    Returns the component currently being rendered.

    This is the top item of the current renderer render stack and is used by
    hooks to access component-local state.

    Returns:
        The currently rendering [`Component`][flet.Component].

    Raises:
        RuntimeError: If called outside an active component render frame.
    """
    r = current_renderer()
    if not r._render_stack:
        raise RuntimeError("Hooks must be called inside a component render.")
    return r._render_stack[-1]


def value_equal(a, b) -> bool:
    """
    Compares two values with tolerant semantics for reactive updates.

    Comparison order:
    - identity check (`a is b`);
    - equality check (`a == b`) with exception suppression;
    - special-case `float('nan')` so NaN compares equal to NaN.

    Args:
        a: First value.
        b: Second value.

    Returns:
        `True` when values are considered equivalent for change detection;
        otherwise `False`.
    """
    # Fast path
    if a is b:
        return True
    # Handle normal equality
    try:
        if a == b:
            return True
    except Exception:
        pass
    # Treat NaN == NaN as equal (like JS Object.is)
    return (
        isinstance(a, float)
        and isinstance(b, float)
        and math.isnan(a)
        and math.isnan(b)
    )


def shallow_compare_args(
    prev_args: Sequence[Any],
    args: Sequence[Any],
) -> bool:
    """
    Performs shallow positional-argument comparison.

    Two argument sequences are considered equal when they are the same object,
    or when they have equal length and each pair is either identical
    (`is`) or equal (`==`).

    Args:
        prev_args: Previously stored positional arguments.
        args: New positional arguments.

    Returns:
        `True` if arguments are shallow-equal; otherwise `False`.
    """
    if prev_args is args:
        return True
    if len(prev_args) != len(args):
        return False
    return all(not (a is not b and a != b) for a, b in zip(prev_args, args))


def shallow_compare_kwargs(
    prev_kwargs: dict[str, Any],
    kwargs: dict[str, Any],
) -> bool:
    """
    Performs shallow keyword-argument comparison.

    Two mappings are considered equal when they are the same object, have the
    same key set, and each corresponding value is either identical (`is`) or
    equal (`==`).

    Args:
        prev_kwargs: Previously stored keyword arguments.
        kwargs: New keyword arguments.

    Returns:
        `True` if keyword arguments are shallow-equal; otherwise `False`.
    """
    if prev_kwargs is kwargs:
        return True
    if prev_kwargs.keys() != kwargs.keys():
        return False
    for k in prev_kwargs:
        a, b = prev_kwargs[k], kwargs[k]
        if a is not b and a != b:
            return False
    return True


def shallow_compare_args_and_kwargs(
    prev_args: tuple[Any, ...],
    prev_kwargs: dict[str, Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> bool:
    """
    Performs combined shallow comparison of positional and keyword arguments.

    Args:
        prev_args: Previously stored positional arguments.
        prev_kwargs: Previously stored keyword arguments.
        args: New positional arguments.
        kwargs: New keyword arguments.

    Returns:
        `True` only if both positional and keyword arguments are shallow-equal.
    """
    return shallow_compare_args(prev_args, args) and shallow_compare_kwargs(
        prev_kwargs, kwargs
    )
