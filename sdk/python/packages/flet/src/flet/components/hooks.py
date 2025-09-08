from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

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
    fn: Callable[[], Any]
    deps: list[Any] | None = None
    cleanup: Callable[[], Any] | None = None
    prev_deps: list[Any] | None = None


@dataclass
class ContextHook(Hook):
    pass
