from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Callable, ParamSpec, TypeVar

from flet.components.hooks.use_memo import use_memo

P = ParamSpec("P")
R = TypeVar("R")


def use_callback(
    fn: Callable[P, R],
    dependencies: Sequence[Any] | None = None,
) -> Callable[P, R]:
    """
    Memoize a function identity between renders.

    Args:
        fn: A function to memoize.
        dependencies: If present, fn is only re-memoized when one of the dependencies
            has changed. If absent, fn is only memoized on initial render.

    Returns:
        A memoized version of the function whose identity is stable between renders.
    """
    # Just memoize the function object itself
    return use_memo(lambda: fn, dependencies)
