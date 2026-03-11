"""
Lightweight module for the ``@value`` decorator and related helpers.

Kept separate from ``base_control`` to avoid circular imports: value types
(Duration, Alignment, etc.) need ``@value`` but are imported transitively by
``base_control`` itself.
"""

import dataclasses
import sys
from dataclasses import dataclass
from typing import Any, Optional

if sys.version_info >= (3, 11):
    from typing import dataclass_transform
else:
    from typing_extensions import dataclass_transform

__all__ = [
    "Prop",
    "Value",
    "value",
]

_UNSET = object()
"""Sentinel for "field not yet in _values" (distinct from None)."""


class Prop:
    """
    Descriptor for sparse property tracking on ``BaseControl`` and ``Value``
    types.

    Each public, non-skip field gets replaced by a ``Prop`` instance by
    ``_install_props()``.  The descriptor stores only *non-default* values in
    ``obj._values``, so the frozen diff fast-path only needs to examine the
    union of keys from two objects' ``_values`` dicts rather than scanning
    every declared field.
    """

    __slots__ = ("name", "default")

    def __init__(self, name: str, default: Any = _UNSET) -> None:
        self.name = name
        self.default = default

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        if obj is None:
            return self
        return obj._values.get(self.name, self.default)

    def __set__(self, obj: Any, value: Any) -> None:
        vals = obj._values
        old = vals.get(self.name, _UNSET)
        # Suppress storing the declared default during construction so
        # that _values only holds genuinely non-default values.
        if old is _UNSET and value == self.default:
            return
        if old is not _UNSET and old == value:
            return  # no change — skip everything
        # Frozen controls must not be mutated after construction.
        if hasattr(obj, "_frozen"):
            raise RuntimeError("Frozen controls cannot be updated.") from None
        if value == self.default:
            vals.pop(self.name, None)  # restore sparseness when back to default
        else:
            vals[self.name] = value
        obj._dirty[self.name] = None
        if hasattr(obj, "_notify"):
            obj._notify(self.name, value)


def _install_props(cls: type) -> None:
    """
    Replace public dataclass fields with ``Prop`` descriptors and record
    non-Prop fields in ``cls._structural_fields``.
    """
    structural: set[str] = set()
    prop_defaults: dict = {}
    event_fields: set[str] = set()
    root_defaults: dict = {}
    override_props: dict = {}

    for f in dataclasses.fields(cls):
        if f.metadata.get("skip", False):
            continue
        can_use_prop = (
            not f.name.startswith("_")
            and f.init is not False
            and f.default_factory is dataclasses.MISSING  # type: ignore[misc]
        )
        if can_use_prop:
            if not isinstance(getattr(cls, f.name, None), Prop):
                default = f.default if f.default is not dataclasses.MISSING else _UNSET
                setattr(cls, f.name, Prop(name=f.name, default=default))
            prop = getattr(cls, f.name)
            prop_defaults[f.name] = prop.default

            if f.name.startswith("on_") and f.metadata.get("event", True):
                event_fields.add(f.name)

            root_default = _UNSET
            for base in reversed(cls.__mro__):
                base_dc_fields = getattr(base, "__dataclass_fields__", None)
                if base_dc_fields and f.name in base_dc_fields:
                    bf = base_dc_fields[f.name]
                    if bf.default is not dataclasses.MISSING:
                        root_default = bf.default
                    break
            root_defaults[f.name] = root_default

            if (
                prop.default is not _UNSET
                and root_default is not _UNSET
                and prop.default != root_default
            ):
                override_props[f.name] = prop.default
        else:
            structural.add(f.name)

    cls._structural_fields = frozenset(structural)  # type: ignore[attr-defined]
    cls._prop_defaults = prop_defaults  # type: ignore[attr-defined]
    cls._event_fields = frozenset(event_fields)  # type: ignore[attr-defined]
    cls._root_defaults = root_defaults  # type: ignore[attr-defined]
    cls._override_props = override_props  # type: ignore[attr-defined]


class _ValueMeta(type):
    def __instancecheck__(cls, instance: Any) -> bool:
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass: type) -> bool:
        return bool(getattr(subclass, "_is_flet_value", False))


class Value(metaclass=_ValueMeta):
    """
    Marker class for non-control value types that have sparse ``_values``
    tracking enabled via ``@value``.

    ``@value`` handles all setup — you never need to inherit from this
    class explicitly.  It is exposed so that ``isinstance(obj, Value)``
    checks work in the diff machinery.
    """


@dataclass_transform()
def value(
    cls: Optional[type] = None,
    **dataclass_kwargs: Any,
) -> Any:
    """
    Decorator for non-control value types to enable sparse ``_values``
    tracking.

    Applies ``@dataclass`` (passing *dataclass_kwargs*) and installs ``Prop``
    descriptors via ``_install_props``.  No base class is required — the
    decorator wraps ``__init__`` to inject ``_values`` and ``_dirty`` before
    the first ``Prop.__set__`` call, and registers the class as a
    ``Value`` subclass for isinstance checks.

    Usage::

        @value
        class TextStyle:
            color: Optional[str] = None
            size: Optional[float] = None


        # or with explicit dataclass kwargs:
        @value(eq=False)
        class TextStyle: ...
    """

    def _apply(cls: type) -> type:
        cls = dataclass(**dataclass_kwargs)(cls)
        _install_props(cls)
        cls._is_flet_value = True

        orig_init = cls.__init__

        def _value_init(self: Any, *args: Any, **kwargs: Any) -> None:
            object.__setattr__(self, "_values", {})
            object.__setattr__(self, "_dirty", {})
            orig_init(self, *args, **kwargs)
            self._dirty.clear()  # reset after construction

        cls.__init__ = _value_init

        return cls

    if cls is not None:
        return _apply(cls)
    return _apply
