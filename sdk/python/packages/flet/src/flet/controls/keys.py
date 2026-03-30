from dataclasses import field
from typing import Optional, Union

__all__ = [
    "Key",
    "KeyValue",
    "ScrollKey",
    "ValueKey",
]


def _lazy_value(cls=None, **kwargs):
    """Deferred proxy for ``value`` to avoid circular import with base_control."""
    from flet.controls.base_control import value as _v

    if cls is not None:
        return _v(cls)
    if kwargs:
        return _v(**kwargs)
    return _v()


@_lazy_value
class Key:
    """
    Base class for control keys.

    Concrete subclasses define `_type` and therefore behavior on the Flutter
    side. Use [`ValueKey`][flet.] for general control identity and
    [`ScrollKey`][flet.] for scroll-target lookups.
    """

    value: Union[str, int, float, bool]
    """
    Stable primitive identifier used to match a control.
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)
    """Discriminator used on Flutter end to select the key kind."""

    def __str__(self) -> str:
        return str(self.value)


@_lazy_value
class ValueKey(Key):
    """
    General-purpose key for control identity.

    Prefer it when you need a stable identifier across rebuilds but do not need
    scroll-specific behavior.
    """

    def __post_init__(self):
        self._type = "value"


@_lazy_value
class ScrollKey(Key):
    """
    Key type used for imperative scroll targeting.

    Use this key to identify an item when calling
    [`ScrollableControl.scroll_to()`][flet.ScrollableControl.scroll_to] with
    `scroll_key`.
    """

    def __post_init__(self):
        self._type = "scroll"


KeyValue = Union[ValueKey, ScrollKey, str, int, float, bool]
"""Type alias for control key values.

Represents keys as either:
- a [`ValueKey`][flet.] or [`ScrollKey`][flet.] object,
- or a primitive `str`, `int`, `float`, or `bool` value.
"""
