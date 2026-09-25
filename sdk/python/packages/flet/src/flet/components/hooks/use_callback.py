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
        dependencies: Values the function depends on. If absent, the `fn` passed on
            each render is returned as is. If empty, the `fn` from the first render
            is kept. Otherwise, it is replaced only when one of the dependencies has
            changed.

    Returns:
        The memoized function. The same function object is returned on every render
            until it is replaced.
    """
    # Just memoize the function object itself
    return use_memo(lambda: fn, dependencies)
