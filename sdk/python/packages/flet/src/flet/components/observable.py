from __future__ import annotations

import contextlib
import weakref
from collections.abc import Iterable
from typing import Any, Callable, Optional

# ---------- Core notifier ----------

Listener = Callable[[Any, Optional[str]], None]  # (sender, field|None)


class Observable:
    """
    Base class: notifies when fields change; auto-wraps lists/dicts to be observable.
    """

    @property
    def __listeners(self):
        storage_name = "_Observable__listeners_storage"  # different name
        try:
            return object.__getattribute__(self, storage_name)
        except AttributeError:
            ws = weakref.WeakSet()
            object.__setattr__(self, storage_name, ws)
            return ws

    # --- subscribe / batching ---
    def subscribe(self, fn: Listener) -> Callable[[], None]:
        self.__listeners.add(fn)

        def dispose():
            with contextlib.suppress(KeyError):
                self.__listeners.remove(fn)

        return dispose

    def _notify(self, field: str | None):
        for fn in list(self.__listeners):
            fn(self, field)

    # --- collection wrappers ---
    def _wrap_if_collection(self, name: str, value: Any) -> Any:
        # Wrap plain list/dict so in-place mutations notify this object
        if isinstance(value, list) and not isinstance(value, ObservableList):
            return ObservableList(self, name, value)
        if isinstance(value, dict) and not isinstance(value, ObservableDict):
            return ObservableDict(self, name, value)
        return value

    # --- attribute interception ---
    def __setattr__(self, name: str, value: Any):
        if name.startswith("_Observable__"):
            object.__setattr__(self, name, value)
            return
        value = self._wrap_if_collection(name, value)
        old = object.__getattribute__(self, name) if hasattr(self, name) else None
        if old is not value:  # identity check; use != if you prefer value semantics
            object.__setattr__(self, name, value)
            self._notify(name)

    def __delattr__(self, name: str):
        existed = hasattr(self, name)
        object.__delattr__(self, name)
        if existed:
            self._notify(name)


# ---------- Observable collections ----------


class ObservableList(list):
    """List that notifies its owner Observable on mutation."""

    __slots__ = ("_owner_ref", "_field")

    def __init__(self, owner: Observable, field: str, iterable: Iterable = ()):
        super().__init__(iterable)
        self._owner_ref = weakref.ref(owner)
        self._field = field

    # mark owner dirty
    def _touch(self):
        owner = self._owner_ref()
        if owner:
            owner._notify(self._field)

    # ensure nested collections get wrapped, too
    def _wrap(self, v):
        owner = self._owner_ref()
        return owner._wrap_if_collection(self._field, v) if owner else v

    # mutators
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
    """Dict that notifies its owner Observable on mutation."""

    __slots__ = ("_owner_ref", "_field")

    def __init__(self, owner: Observable, field: str, mapping: dict | Iterable = ()):
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

    # mutators
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
