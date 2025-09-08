from collections.abc import Callable
from typing import TypeVar, cast

from typing_extensions import Protocol

ContextValueT = TypeVar("ContextValueT")

T = TypeVar("T")  # context value type
ProviderResultT = TypeVar(
    "ProviderResultT", covariant=True
)  # return type of the callback/provider


class ContextProvider(Protocol[T]):
    default_value: T

    # Generic call: whatever the callback returns (ProviderResultT),
    # the provider returns too.
    def __call__(
        self, value: T, callback: Callable[[], ProviderResultT]
    ) -> ProviderResultT: ...


def create_context(default_value: T) -> ContextProvider[T]:
    def provider(value: T, callback: Callable[[], ProviderResultT]) -> ProviderResultT:  # type: ignore[type-var]
        # TODO real impl: push(value); out = callback(); pop(); return out
        return callback()  # type: ignore[return-value]

    p = cast(ContextProvider[T], provider)
    p.default_value = default_value
    return p


def use_context(context):
    # component = current_component()
    # if context not in component.contexts:
    #     component.contexts[context] = context.default_value
    # return component.contexts[context]
    return context.default_value
