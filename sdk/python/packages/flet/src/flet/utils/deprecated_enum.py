from __future__ import annotations

import warnings
from enum import EnumMeta

__all__ = ["DeprecatedEnumMeta"]


class DeprecatedEnumMeta(EnumMeta):
    """Enum metaclass that supports deprecation aliases.

    Enums can declare `_deprecated_members_` as a mapping of alias name to a tuple
    containing the canonical member name and a deprecation message. Accessing an alias
    returns the canonical member while emitting a `DeprecationWarning`.
    """

    def _resolve_deprecated(cls, name: str):
        deprecated = getattr(cls, "_deprecated_members_", {})
        info = deprecated.get(name)
        if not info:
            return None
        target_name, message = info
        warnings.warn(
            f"{cls.__name__}.{name} is deprecated. {message}",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(cls, target_name)

    def __getattr__(cls, name: str):
        member = cls._resolve_deprecated(name)
        if member is not None:
            return member
        return super().__getattr__(name)

    def __getitem__(cls, name: str):
        member = cls._resolve_deprecated(name)
        if member is not None:
            return member
        return super().__getitem__(name)
