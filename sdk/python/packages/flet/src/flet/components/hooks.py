import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from flet.components.component_owned import ComponentOwned
from flet.components.observable import ObservableSubscription

if TYPE_CHECKING:
    pass


@dataclass()
class Hook(ComponentOwned):
    pass


@dataclass
class StateHook(Hook):
    value: Any
    subscription: ObservableSubscription | None = None
    version: int = 0


@dataclass
class EffectHook(Hook):
    setup: Callable[[], Any | Awaitable[Any]]
    cleanup: Callable[[], Any | Awaitable[Any]] | None = None
    deps: list[Any] | None = None
    prev_deps: list[Any] | None = None

    # runtime
    _setup_task: asyncio.Task | None = None  # last scheduled setup task
    _cleanup_task: asyncio.Task | None = None  # last scheduled cleanup task

    def cancel(self):
        if self._setup_task and not self._setup_task.done():
            self._setup_task.cancel()
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()


@dataclass
class ContextHook(Hook):
    pass


MemoValueT = TypeVar("MemoValueT")


@dataclass
class MemoHook(Hook, Generic[MemoValueT]):
    value: MemoValueT | None = None
    prev_deps: list[Any] | None = None
