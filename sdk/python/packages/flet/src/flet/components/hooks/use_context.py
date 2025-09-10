from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar, cast

from typing_extensions import Protocol

from flet.components.hooks.hook import Hook
from flet.components.observable import Observable
from flet.components.utils import current_component, current_renderer


@dataclass
class ContextHook(Hook):
    pass


ContextValueT = TypeVar("ContextValueT")

T = TypeVar("T")  # context value type
ProviderResultT = TypeVar(
    "ProviderResultT", covariant=True
)  # return type of the callback/provider


class ContextProvider(Protocol[T]):
    default_value: T
    _key: object

    # Generic call: whatever the callback returns (ProviderResultT),
    # the provider returns too.
    def __call__(
        self, value: T, callback: Callable[[], ProviderResultT]
    ) -> ProviderResultT: ...


def create_context(default_value: T) -> ContextProvider[T]:
    key = object()

    def provider(value: T, callback: Callable[[], ProviderResultT]) -> ProviderResultT:  # type: ignore[type-var]
        r = current_renderer()
        r.push_context(key, value)
        try:
            return callback()  # type: ignore[return-value]
        finally:
            r.pop_context(key)

    p = cast(ContextProvider[T], provider)
    p.default_value = default_value
    p._key = key
    return p


def use_context(context: ContextProvider[T]) -> T:
    component = current_component()
    component.use_hook(lambda: ContextHook(component))

    value = cast(T, context.default_value)
    # look up the component tree for the nearest context provider
    comp = component
    while comp:
        if context._key in comp._state.contexts:
            value = cast(T, comp._state.contexts[context._key])
            break
        comp = comp._parent_component() if comp._parent_component else None

    if isinstance(value, Observable):
        component._attach_observable_subscription(value)

    return value


context = use_context  # alias for convenience
