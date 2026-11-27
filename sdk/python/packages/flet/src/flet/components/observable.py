from __future__ import annotations

import contextlib
import datetime
import enum
import numbers
import threading
import weakref
from collections.abc import Sequence
from dataclasses import InitVar, dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional, cast

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
        List and dict values are copied into observable collections when they
        are assigned to a field or added to such a collection, so later changes
        to them notify the field. Assigning `other.items` to `obj.items` copies
        it too: the two fields don't share one list.

        Assigning a field the mutable object it already holds, as Python does
        after an in-place operator such as `obj.tags |= {"a"}` on a set,
        notifies, since the object may have changed in place.

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
    _manual_version = 0

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
        if field is None:
            self._manual_version += 1
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
        Wrap list/dict values into observable collections reporting to `name`.

        Plain lists and dicts are copied into observable collections, and so
        are observable collections that report to another observable or field,
        so that later changes notify this field. Nested lists and dicts are
        wrapped too; a list or dict that appears several times in `value`,
        including inside itself, is wrapped once.

        Args:
            name: Field name being assigned.
            value: Field value to evaluate.

        Returns:
            Observable collection for `list`/`dict` values, otherwise the
            original value.
        """

        if (
            isinstance(value, _ObservableCollection)
            and value._owner_ref() is self
            and value._field == name
        ):
            return value
        if isinstance(value, list):
            cls = ObservableList
        elif isinstance(value, dict):
            cls = ObservableDict
        else:
            return value
        memo = getattr(_wrapping, "memo", None)
        if memo is not None:
            wrapped = memo.get(id(value))
            return wrapped if wrapped is not None else cls(self, name, value)
        _wrapping.memo = {}
        try:
            return cls(self, name, value)
        finally:
            _wrapping.memo = None

    # attribute interception
    def __setattr__(self, name: str, value: Any):
        if name.startswith("_"):  # private/internal, don't notify
            object.__setattr__(self, name, value)
            return
        value = self._wrap_if_collection(name, value)
        old = object.__getattribute__(self, name) if hasattr(self, name) else None
        object.__setattr__(self, name, value)
        if value is old:
            # The same object is assigned back, as Python does after an
            # in-place operator such as `obj.tags |= {"a"}`. A mutable value
            # may have changed in place; observable collections reporting to
            # this field have notified already.
            if not isinstance(value, _IMMUTABLE_TYPES) and not isinstance(
                value, _ObservableCollection
            ):
                self._notify(name)
        elif not value_equal(old, value):
            self._notify(name)

    def __delattr__(self, name: str):
        existed = hasattr(self, name)
        object.__delattr__(self, name)
        if existed:
            self._notify(name)

    def __repr__(self):
        return f"{super().__repr__()} (version={self.__version__})"


# Values that can't change in place, so assigning the same one again to a
# field is not a change.
_IMMUTABLE_TYPES = (
    type(None),
    numbers.Number,
    str,
    bytes,
    tuple,
    frozenset,
    range,
    enum.Enum,
    datetime.date,
    datetime.time,
    datetime.timedelta,
)


# Observable collections -----------------------------------------

# Collections wrapped so far in the current `_wrap_if_collection()` call, by
# the id of their source, so shared and self-containing values are wrapped once.
_wrapping = threading.local()


def _register_wrapping(source: Any, wrapped: _ObservableCollection):
    memo = getattr(_wrapping, "memo", None)
    if memo is not None:
        memo[id(source)] = wrapped


class _CollectionRevision:
    """Shared by hook snapshots until the watched collection tree changes."""

    __slots__ = ("__weakref__", "current")

    def __init__(self):
        self.current = True


class _ObservableCollection:
    """
    Base for collections that report changes to a field of an observable.

    Hook snapshots share a revision until this collection or a descendant
    changes. Descendants hold weak references to watched ancestor revisions.
    """

    __slots__ = ()

    _owner_ref: weakref.ref
    _field: str

    _revision: _CollectionRevision | None
    _ancestor_revisions: weakref.WeakSet[_CollectionRevision] | None
    _has_nested: bool

    def _init_collection(self, owner: Observable, field: str, source: Any):
        self._owner_ref = weakref.ref(owner)
        self._field = field
        self._revision = None
        self._ancestor_revisions = None
        self._has_nested = False
        _register_wrapping(source, self)

    def _touch(self):
        """Invalidate snapshots of this collection and notify its owner."""
        if self._revision is not None:
            self._revision.current = False
        if self._ancestor_revisions:
            for revision in self._ancestor_revisions:
                revision.current = False
            self._ancestor_revisions.clear()
        owner = self._owner_ref()
        if owner is not None:
            owner._notify(self._field)

    def _capture_revision(self) -> _CollectionRevision:
        if self._revision is not None and self._revision.current:
            return self._revision

        revision = _CollectionRevision()
        self._revision = revision
        if self._has_nested:
            # Register only reachable descendants. A structural edit invalidates
            # this revision, so the next capture follows the updated tree.
            pending = [self]
            seen = {id(self)}
            while pending:
                node = pending.pop()
                values = node.values() if isinstance(node, dict) else cast(list, node)
                for child in values:
                    if (
                        not isinstance(child, _ObservableCollection)
                        or id(child) in seen
                    ):
                        continue
                    seen.add(id(child))
                    if child._ancestor_revisions is None:
                        child._ancestor_revisions = weakref.WeakSet()
                    child._ancestor_revisions.add(revision)
                    if child._has_nested:
                        pending.append(child)
        return revision

    def _wrapper(self) -> Callable[[Any], Any]:
        """
        Return a function that wraps values before they are stored.

        The owner is resolved once, so bulk operations don't dereference the
        weak reference for every item.
        """

        owner = self._owner_ref()
        if owner is None:
            return self._wrap
        field = self._field
        wrap = owner._wrap_if_collection

        def wrapper(v):
            if isinstance(v, (list, dict)):
                self._has_nested = True
                return wrap(field, v)
            return v

        return wrapper

    def _wrap(self, v):
        """
        Wrap a nested collection into an observable variant before storing.

        Args:
            v: Value being inserted into the collection.

        Returns:
            Wrapped value when applicable.
        """

        if not isinstance(v, (list, dict)):
            return v
        owner = self._owner_ref()
        self._has_nested = True
        return owner._wrap_if_collection(self._field, v) if owner is not None else v


class ObservableList(_ObservableCollection, list):
    """
    List wrapper that reports mutating operations to its owning observable.
    """

    __slots__ = (
        "_ancestor_revisions",
        "_field",
        "_has_nested",
        "_owner_ref",
        "_revision",
    )

    def __init__(self, owner: Observable, field: str, iterable=()):
        self._init_collection(owner, field, iterable)
        super().__init__(map(self._wrapper(), iterable))

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
        objects. Observers are notified when at least one item was appended,
        also when the iterable raises after some items were appended.
        """

        size = len(self)
        try:
            if it is self:
                super().extend(self)
            else:
                super().extend(map(self._wrapper(), it))
        finally:
            if len(self) != size:
                self._touch()

    def __iadd__(self, other):
        """
        Extend list in place (`+=`) and notify observers.

        As with `list`, an operand whose type defines `__radd__()` is asked
        first, and its result replaces the list when it is not
        `NotImplemented`.

        Observers are notified before Python assigns the list back to its
        field, so a subscriber that replaces the field during `+=` has its
        replacement overwritten. Call `extend()` to keep such a replacement.
        """

        radd = getattr(type(other), "__radd__", None)
        if radd is not None:
            result = radd(other, self)
            if result is not NotImplemented:
                return result
        self.extend(other)
        return self

    def __imul__(self, n):
        """
        Repeat list items in place (`*=`) and notify observers.

        As with `list`, an operand whose type defines `__rmul__()` is asked
        first, and its result replaces the list when it is not
        `NotImplemented`.

        Observers are notified before Python assigns the list back to its
        field, so a subscriber that replaces the field during `*=` has its
        replacement overwritten.
        """

        rmul = getattr(type(n), "__rmul__", None)
        if rmul is not None:
            result = rmul(n, self)
            if result is not NotImplemented:
                return result
        size = len(self)
        super().__imul__(n)
        if len(self) != size:
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
        """

        wrap = self._wrapper()
        v = [wrap(x) for x in v] if isinstance(i, slice) else wrap(v)
        super().__setitem__(i, v)
        self._touch()

    def __delitem__(self, i):
        super().__delitem__(i)
        self._touch()


class ObservableDict(_ObservableCollection, dict):
    """
    Dict wrapper that reports mutating operations to its owning observable.
    """

    __slots__ = (
        "_ancestor_revisions",
        "_field",
        "_has_nested",
        "_owner_ref",
        "_revision",
    )

    def __init__(self, owner: Observable, field: str, mapping=()):
        self._init_collection(owner, field, mapping)
        super().__init__(mapping)
        wrap = self._wrapper()
        for k, v in list(dict.items(self)):
            if isinstance(v, (list, dict)):
                dict.__setitem__(self, k, wrap(v))

    def __setitem__(self, k, v):
        """
        Set a key and notify observers.
        """

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

    def update(self, /, *a, **k):
        """
        Update mapping with values and notify observers.

        Takes the same arguments as `dict.update()` and inserts entries in the
        same order: the mapping's keys or the key-value pairs first, one at a
        time, then the keywords. List and dict values are wrapped as they are
        inserted. Observers are notified once when at least one entry was
        inserted, also when the input raises after some entries were inserted.
        """

        if len(a) > 1:
            raise TypeError(f"update expected at most 1 argument, got {len(a)}")
        wrap = self._wrapper()
        setitem = dict.__setitem__
        changed = False
        try:
            if a:
                other = a[0]
                if type(other) is dict:
                    # Fast path: merge at C speed, then wrap collection values.
                    dict.update(self, other)
                    changed = bool(other)
                    for kk, vv in other.items():
                        if isinstance(vv, (list, dict)):
                            setitem(self, kk, wrap(vv))
                elif hasattr(other, "keys"):
                    for kk in other.keys():  # noqa: SIM118
                        setitem(self, kk, wrap(other[kk]))
                        changed = True
                else:
                    for kk, vv in other:
                        setitem(self, kk, wrap(vv))
                        changed = True
            for kk, vv in k.items():
                setitem(self, kk, wrap(vv))
                changed = True
        finally:
            if changed:
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


# Hook dependencies ---------------------------------------------


class _CollectionDependency:
    """
    An observable collection in a hook's dependencies, with its version when the
    dependencies were captured.

    The same collection is unchanged only while its version stays the same, so
    `use_memo` and `use_effect` see in-place changes such as `items.append(x)`.
    Different collections compare by their items, as plain lists and dicts do.
    """

    __slots__ = ("collection", "manual_version", "revision")

    def __init__(self, collection: _ObservableCollection):
        self.collection = collection
        self.revision = collection._capture_revision()
        self.manual_version = self._owner_version()

    def _owner_version(self) -> int:
        owner = self.collection._owner_ref()
        return owner._manual_version if owner is not None else 0

    def _is_current(self) -> bool:
        return self.revision.current and self.manual_version == self._owner_version()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _CollectionDependency):
            if self.collection is other.collection:
                return (
                    self.revision is other.revision
                    and self.manual_version == other.manual_version
                )
            if not other._is_current():
                return False
            other = other.collection
        # Item equality is meaningful only while the captured contents survive.
        return self._is_current() and value_equal(self.collection, other)

    __hash__ = None  # type: ignore[assignment]


def capture_dependencies(dependencies: Sequence[Any]) -> list[Any]:
    """
    Snapshot hook dependencies for comparison on the next render.

    Observable lists and dicts are recorded with their version, since they stay
    the same object when they change in place.
    """

    return [
        _CollectionDependency(d) if isinstance(d, _ObservableCollection) else d
        for d in dependencies
    ]
