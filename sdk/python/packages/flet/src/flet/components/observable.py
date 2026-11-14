from __future__ import annotations

import contextlib
import operator
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
    Makes a class observable by mixing in :class:`~flet.Observable`.
    Can be applied to any class including `dataclasses.dataclass`.
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

    Note:
        Listeners are called synchronously. With augmented assignments such as
        `obj.items += [x]`, `*=` on lists and `|=` on dicts, they run before
        Python assigns the result back to the field, so a listener that
        replaces `obj.items` at that moment is overwritten. Direct calls such
        as `obj.items.extend([x])` keep the listener's replacement.
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


# eq=False: see ComponentOwned. `Component._detach_observable_subscription` matches
# subscriptions with `in`/`list.remove`, so a field-based `__eq__` detaches the wrong
# one and leaks the other (see #6776).
@dataclass(eq=False)
class ObservableSubscription(ComponentOwned):
    """
    Lifecycle helper that binds an observable object to a component update cycle.

    The subscription listens for observable changes and schedules re-render of
    the owning component while the component is alive.
    """

    observable: InitVar[Observable]
    """
    Observable object to subscribe to.
    """

    def __post_init__(self, owner: Component, observable: Observable) -> None:
        super().__post_init__(owner)
        self.__disposer = observable.subscribe(self.__on_change)

    def dispose(self):
        """
        Cancel the underlying observable subscription if it is still active.
        """

        if callable(self.__disposer):
            self.__disposer()
            self.__disposer = None

    def __on_change(self, _sender, _field):
        """
        Schedule owner component update when observable state changes.

        Args:
            _sender: Observable object that emitted change.
            _field: Name of changed field, or `None` for generic change.
        """

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
        """
        Lazily initialized weak set of registered listener callbacks.
        """

        storage_name = "_Observable__listeners_storage"
        try:
            return object.__getattribute__(self, storage_name)
        except AttributeError:
            ws = weakref.WeakSet()
            object.__setattr__(self, storage_name, ws)
            return ws

    # subscribe / notify
    def subscribe(self, fn: Listener) -> Callable[[], None]:
        """
        Register a change listener.

        Args:
            fn: Listener callback receiving `(sender, field)`.

        Returns:
            A disposer function that unsubscribes the listener.
        """

        self.__listeners.add(fn)

        def dispose():
            """
            Remove the subscribed listener from this observable.
            """
            with contextlib.suppress(KeyError):
                self.__listeners.remove(fn)

        return dispose

    def _notify(self, field: str | None):
        """
        Notify all listeners about a field change.

        Args:
            field: Changed field name, or `None` for a generic change.
        """

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
        """
        Wrap plain list/dict values into observable collection wrappers.

        Args:
            name: Field name being assigned.
            value: Field value to evaluate.

        Returns:
            Observable collection wrapper for `list`/`dict` values, otherwise
            the original value.
        """

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

_MISSING = object()


def _is_written_back(container, current: Any, value: Any) -> bool:
    """
    Tell whether `value` is the observable child already stored in a slot.

    Python writes the result of an augmented assignment such as
    `d["items"] += [1]` back into the slot. The child has notified already, so
    writing the identical child back to the same owner and field is a no-op.

    Args:
        container: Observable list or dict that holds the slot.
        current: Value in the slot, or `_MISSING` when the slot is empty.
        value: Value being written into the slot.

    Returns:
        `True` when `value` is `current` and reports to the same owner and field.
    """

    return (
        value is current
        and isinstance(value, (ObservableList, ObservableDict))
        and value._owner_ref() is container._owner_ref()
        and value._field == container._field
    )


class ObservableList(list):
    """
    List wrapper that reports mutating operations to its owning observable.
    """

    __slots__ = ("_owner_ref", "_field")

    def __init__(self, owner: Observable, field: str, iterable=()):
        super().__init__(iterable)
        self._owner_ref = weakref.ref(owner)
        self._field = field

    def _touch(self):
        """
        Emit a change notification for the parent field.
        """

        owner = self._owner_ref()
        if owner:
            owner._notify(self._field)

    def _wrap(self, v):
        """
        Wrap nested collections into observable variants before storing.

        Args:
            v: Value being inserted into the list.

        Returns:
            Wrapped value when applicable.
        """

        owner = self._owner_ref()
        return owner._wrap_if_collection(self._field, v) if owner else v

    def append(self, x):
        """
        Append an item and notify observers.
        """

        super().append(self._wrap(x))
        self._touch()

    def extend(self, it):
        """
        Extend list with iterable items and notify observers.

        Items are appended one at a time, as with `list.extend()`.
        `xs.extend(xs)` appends the list's current items once, as the same
        objects. If the iterable raises after some items were appended,
        observers are still notified before the error propagates.
        """

        size = len(self)
        try:
            if it is self:
                super().extend(self)
            else:
                super().extend(self._wrap(v) for v in it)
        except BaseException:
            if len(self) != size:
                self._touch()
            raise
        self._touch()

    def __iadd__(self, other):
        """
        Extend list in place (`+=`) and notify observers.

        Observers are notified before Python assigns the list back to its
        field, so a subscriber that replaces the field during `+=` has its
        replacement overwritten. Call `extend()` to keep such a replacement.
        """

        self.extend(other)
        return self

    def __imul__(self, n):
        """
        Repeat list items in place (`*=`) and notify observers.

        Observers are notified before Python assigns the list back to its
        field, so a subscriber that replaces the field during `*=` has its
        replacement overwritten.
        """

        super().__imul__(n)
        self._touch()
        return self

    def insert(self, i, x):
        """
        Insert an item at a specific index and notify observers.
        """

        super().insert(i, self._wrap(x))
        self._touch()

    def remove(self, x):
        """
        Remove first matching item and notify observers.
        """

        super().remove(x)
        self._touch()

    def clear(self):
        """
        Remove all items and notify observers.
        """

        super().clear()
        self._touch()

    def sort(self, *a, **k):
        """
        Sort items in place and notify observers.
        """

        super().sort(*a, **k)
        self._touch()

    def reverse(self):
        """
        Reverse item order in place and notify observers.
        """

        super().reverse()
        self._touch()

    def pop(self, i=-1):
        """
        Remove and return an item by index, then notify observers.

        Args:
            i: Index to pop. Defaults to the last item.

        Returns:
            Removed item.
        """

        v = super().pop(i)
        self._touch()
        return v

    def __setitem__(self, i, v):
        """
        Set an item or a slice and notify observers.

        Writing the item's own observable child back to its index, as Python
        does after `xs[0] += [1]`, changes nothing and doesn't notify again.
        An index object's `__index__()` is called once, as with `list`.
        """

        if not isinstance(i, slice):
            try:
                i = operator.index(i)
            except TypeError:
                pass
            else:
                current = (
                    list.__getitem__(self, i)
                    if -len(self) <= i < len(self)
                    else _MISSING
                )
                if _is_written_back(self, current, v):
                    return
        super().__setitem__(i, self._wrap(v))
        self._touch()

    def __delitem__(self, i):
        super().__delitem__(i)
        self._touch()


class ObservableDict(dict):
    """
    Dict wrapper that reports mutating operations to its owning observable.
    """

    __slots__ = ("_owner_ref", "_field")

    def __init__(self, owner: Observable, field: str, mapping=()):
        super().__init__(mapping)
        self._owner_ref = weakref.ref(owner)
        self._field = field

    def _touch(self):
        """
        Emit a change notification for the parent field.
        """

        owner = self._owner_ref()
        if owner:
            owner._notify(self._field)

    def _wrap(self, v):
        """
        Wrap nested collections into observable variants before storing.

        Args:
            v: Value being inserted into the dict.

        Returns:
            Wrapped value when applicable.
        """

        owner = self._owner_ref()
        return owner._wrap_if_collection(self._field, v) if owner else v

    def __setitem__(self, k, v):
        """
        Set a key and notify observers.

        Writing the key's own observable child back, as Python does after
        `d["items"] += [1]`, changes nothing and doesn't notify again.
        """

        if _is_written_back(self, dict.get(self, k, _MISSING), v):
            return
        super().__setitem__(k, self._wrap(v))
        self._touch()

    def __delitem__(self, k):
        super().__delitem__(k)
        self._touch()

    def clear(self):
        """
        Remove all entries and notify observers.
        """

        super().clear()
        self._touch()

    def update(self, *a, **k):
        """
        Update mapping with values and notify observers.

        Takes the same arguments as `dict.update()` and inserts entries in the
        same order: the mapping's keys or the key-value pairs first, one at a
        time, then the keywords. List and dict values are wrapped as they are
        inserted. Observers are notified once; if the input raises after some
        entries were inserted, they are notified before the error propagates.
        """

        if len(a) > 1:
            raise TypeError(f"update expected at most 1 argument, got {len(a)}")
        changed = False
        try:
            if a:
                other = a[0]
                if hasattr(other, "keys"):
                    for kk in other.keys():  # noqa: SIM118
                        dict.__setitem__(self, kk, self._wrap(other[kk]))
                        changed = True
                else:
                    for kk, vv in other:
                        dict.__setitem__(self, kk, self._wrap(vv))
                        changed = True
            for kk, vv in k.items():
                dict.__setitem__(self, kk, self._wrap(vv))
                changed = True
        except BaseException:
            if changed:
                self._touch()
            raise
        self._touch()

    def __ior__(self, other):
        """
        Merge a mapping in place (`|=`) and notify observers.

        Observers are notified before Python assigns the dict back to its
        field, so a subscriber that replaces the field during `|=` has its
        replacement overwritten. Call `update()` to keep such a replacement.
        """

        self.update(other)
        return self

    def pop(self, k, *d):
        """
        Remove key and return its value, then notify observers.

        Args:
            k: Key to remove.
            *d: Optional default value.

        Returns:
            Removed value or default.
        """

        v = super().pop(k, *d)
        self._touch()
        return v

    def popitem(self):
        """
        Remove and return the last inserted key-value pair, then notify observers.

        Returns:
            Removed `(key, value)` pair.
        """

        kv = super().popitem()
        self._touch()
        return kv

    def setdefault(self, k, d=None):
        """
        Return value for key, inserting default when key is absent.

        Args:
            k: Key to look up.
            d: Default value to insert when key does not exist.

        Returns:
            Existing or newly inserted value.
        """

        if k not in self:
            super().__setitem__(k, self._wrap(d))
            self._touch()
        return dict.__getitem__(self, k)
