from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Callable, ParamSpec, TypeVar

from flet.hooks.use_memo import use_memo

P = ParamSpec("P")
R = TypeVar("R")


def use_callback(
    fn: Callable[P, R],
    dependencies: Sequence[Any] | None = None,
) -> Callable[P, R]:
    """
    Memoize a function identity between renders.
    - dependencies is None: new function each render
    - dependencies == []  : same function forever (until unmount)
    - else                : new function only when any dep changes
    """
    # Just memoize the function object itself
    return use_memo(lambda: fn, dependencies)


callback = use_callback  # alias for convenience
