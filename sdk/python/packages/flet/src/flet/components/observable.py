from __future__ import annotations

import contextlib
import weakref
from dataclasses import InitVar, dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional

from flet.components.utils import value_equal

if TYPE_CHECKING:
    from flet.components.component import Component

from flet.components.component_owned import ComponentOwned

Listener = Callable[[Any, Optional[str]], None]  # (sender, field|None)


def observable(cls):
    """
    Makes a class observable by mixing in [`Observable`][flet.Observable].
    Can be applied to any class including [`dataclass`][dataclasses.dataclass].
    For dataclasses, decorator can be placed either above or below
    the `@dataclass` decorator.

    Example:
        ```python
        from dataclasses import dataclass
        import flet as ft


        @ft.observable
        @dataclass
        class MyDataClass:
            x: int
            y: int
        ```
    """
    if Observable in cls.__mro__:
        return cls
    # Build a new class whose MRO is (Observable, cls)
    ns = dict(cls.__dict__)
    # Defensive: avoid carrying these special slots over
    ns.pop("__dict__", None)
    ns.pop("__weakref__", None)

    Mixed = type(cls.__name__, (Observable, cls), ns)
    Mixed.__module__ = cls.__module__
    Mixed.__qualname__ = cls.__qualname__
    return Mixed


@dataclass
class ObservableSubscription(ComponentOwned):
    observable: InitVar[Observable]

    def __post_init__(self, owner: Component, observable: Observable) -> None:
        super().__post_init__(owner)
        self.__disposer = observable.subscribe(self.__on_change)

    def dispose(self):
        if callable(self.__disposer):
            self.__disposer()
            self.__disposer = None

    def __on_change(self, _sender, _field):
        if self.component:
            self.component._schedule_update()


class Observable:
    """
    Mixin: notifies when fields change; auto-wraps lists/dicts to be observable.

    Example:
        ```python
        import flet as ft
        from dataclasses import dataclass


        @ft.observable
        @dataclass
        class MyDataClass:
            x: int
            y: int


        obj = MyDataClass(1, 2)


        def listener(sender, field):
            print(f"Changed: {field} in {sender}")


        obj.subscribe(listener)
        obj.x = 3
        obj.y = 4
        ```
    """

    __version__ = 0  # optional version counter

    # listeners store (lazy)
    @property
    def __listeners(self):
        storage_name = "_Observable__listeners_storage"
        try:
            return object.__getattribute__(self, storage_name)
        except AttributeError:
            ws = weakref.WeakSet()
            object.__setattr__(self, storage_name, ws)
            return ws

    # subscribe / notify
    def subscribe(self, fn: Listener) -> Callable[[], None]:
        self.__listeners.add(fn)

        def dispose():
            with contextlib.suppress(KeyError):
                self.__listeners.remove(fn)

        return dispose

    def _notify(self, field: str | None):
        self.__version__ += 1
        for fn in list(self.__listeners):
            fn(self, field)

    def notify(self):
        """
        Manually notify listeners that something changed.
        """
        self._notify(None)

    # collection wrapping
    def _wrap_if_collection(self, name: str, value: Any) -> Any:
        if isinstance(value, list) and not isinstance(value, ObservableList):
            return ObservableList(self, name, value)
        if isinstance(value, dict) and not isinstance(value, ObservableDict):
            return ObservableDict(self, name, value)
        return value

    # attribute interception
    def __setattr__(self, name: str, value: Any):
        if name.startswith("_"):  # private/internal, don't notify
            object.__setattr__(self, name, value)
            return
        value = self._wrap_if_collection(name, value)
        old = object.__getattribute__(self, name) if hasattr(self, name) else None
        object.__setattr__(self, name, value)
        if not value_equal(old, value):
            self._notify(name)

    def __delattr__(self, name: str):
        existed = hasattr(self, name)
        object.__delattr__(self, name)
        if existed:
            self._notify(name)

    def __repr__(self):
        return f"{super().__repr__()} (version={self.__version__})"


# Observable collections -----------------------------------------


class ObservableList(list):
    __slots__ = ("_owner_ref", "_field")

    def __init__(self, owner: Observable, field: str, iterable=()):
        super().__init__(iterable)
        self._owner_ref = weakref.ref(owner)
        self._field = field

    def _touch(self):
        owner = self._owner_ref()
        if owner:
            owner._notify(self._field)

    def _wrap(self, v):
        owner = self._owner_ref()
        return owner._wrap_if_collection(self._field, v) if owner else v

    def append(self, x):
        super().append(self._wrap(x))
        self._touch()

    def extend(self, it):
        super().extend(self._wrap(v) for v in it)
        self._touch()

    def insert(self, i, x):
        super().insert(i, self._wrap(x))
        self._touch()

    def remove(self, x):
        super().remove(x)
        self._touch()

    def clear(self):
        super().clear()
        self._touch()

    def sort(self, *a, **k):
        super().sort(*a, **k)
        self._touch()

    def reverse(self):
        super().reverse()
        self._touch()

    def pop(self, i=-1):
        v = super().pop(i)
        self._touch()
        return v

    def __setitem__(self, i, v):
        super().__setitem__(i, self._wrap(v))
        self._touch()

    def __delitem__(self, i):
        super().__delitem__(i)
        self._touch()


class ObservableDict(dict):
    __slots__ = ("_owner_ref", "_field")

    def __init__(self, owner: Observable, field: str, mapping=()):
        super().__init__(mapping)
        self._owner_ref = weakref.ref(owner)
        self._field = field

    def _touch(self):
        owner = self._owner_ref()
        if owner:
            owner._notify(self._field)

    def _wrap(self, v):
        owner = self._owner_ref()
        return owner._wrap_if_collection(self._field, v) if owner else v

    def __setitem__(self, k, v):
        super().__setitem__(k, self._wrap(v))
        self._touch()

    def __delitem__(self, k):
        super().__delitem__(k)
        self._touch()

    def clear(self):
        super().clear()
        self._touch()

    def update(self, *a, **k):
        super().update(*a, **{kk: self._wrap(vv) for kk, vv in k.items()})
        self._touch()

    def pop(self, k, *d):
        v = super().pop(k, *d)
        self._touch()
        return v

    def popitem(self):
        kv = super().popitem()
        self._touch()
        return kv

    def setdefault(self, k, d=None):
        if k not in self:
            super().__setitem__(k, self._wrap(d))
            self._touch()
        return dict.__getitem__(self, k)
