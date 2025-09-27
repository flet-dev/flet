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
    r = _CURRENT_RENDERER.get()
    if r is None:
        raise RuntimeError(
            "No current renderer is set. Call via Renderer.render(...) "
            "or Renderer.with_context(...)."
        )
    return r


def current_component() -> "Component":
    r = current_renderer()
    if not r._render_stack:
        raise RuntimeError("Hooks must be called inside a component render.")
    return r._render_stack[-1]


def value_equal(a, b) -> bool:
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
    if prev_args is args:
        return True
    if len(prev_args) != len(args):
        return False
    return all(not (a is not b and a != b) for a, b in zip(prev_args, args))


def shallow_compare_kwargs(
    prev_kwargs: dict[str, Any],
    kwargs: dict[str, Any],
) -> bool:
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
    return shallow_compare_args(prev_args, args) and shallow_compare_kwargs(
        prev_kwargs, kwargs
    )
