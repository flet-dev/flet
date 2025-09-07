from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class StateHook:
    value: Any
    disposer: Callable[[], Any] | None = None
    version: int = 0


@dataclass
class EffectHook:
    fn: Callable[[], Any]
    deps: list[Any] | None = None
    cleanup: Callable[[], Any] | None = None
    prev_deps: list[Any] | None = None
