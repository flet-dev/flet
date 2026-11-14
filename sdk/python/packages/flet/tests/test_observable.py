from dataclasses import dataclass, field

import pytest

import flet as ft


class Foo(ft.Observable):
    """Observable with annotated fields and no dataclass."""

    prop_a: str
    prop_b: str


@dataclass
class Bar:
    """Plain dataclass base for `Baz`."""

    f: int
    d: list[int] = field(default_factory=list)


@dataclass
class Baz(Bar, ft.Observable):
    """Observable dataclass that inherits fields from a plain dataclass."""

    prop_c: int = 3
    prop_d: list[int] = field(default_factory=lambda: [1, 2, 3])

    def add_item(self, item: int):
        """Appends `item` to `prop_d`."""
        self.prop_d.append(item)


@dataclass
class Qux(ft.Observable):
    """Observable dataclass with a dict field."""

    prop_e: dict = field(default_factory=dict)

    def update_key(self, key, value):
        """Sets `key` in `prop_e`."""
        self.prop_e[key] = value


@dataclass
class Store(ft.Observable):
    """Observable dataclass with a list field and a dict field."""

    items: list = field(default_factory=list)
    mapping: dict = field(default_factory=dict)


def _watch(obj):
    """Subscribes to `obj` and returns the list of changed field names.

    The listener is stored on `obj`, because observables hold listeners weakly.
    """
    changes = []

    def listener(sender, field):
        changes.append(field)

    obj._test_listener = listener
    obj.subscribe(listener)
    return changes


class TestObservable:
    """Notifications and versioning of observable objects."""

    def test_field_assignment_notifies(self):
        """Assigning a field notifies with the sender and the field name."""
        changes = []

        def subscriber(sender, field):
            changes.append((sender, field))

        foo = Foo()
        foo.subscribe(subscriber)

        foo.prop_a = "test_value"
        assert len(changes) == 1
        assert changes[0][0] == foo
        assert changes[0][1] == "prop_a"

        foo.prop_b = "another_value"
        assert len(changes) == 2
        assert changes[1][0] == foo
        assert changes[1][1] == "prop_b"

    def test_dataclass_subclass_notifies(self):
        """Own, inherited and list fields of an observable dataclass notify."""
        changes = []

        def subscriber(sender, field):
            changes.append((sender, field))

        baz = Baz(42)
        baz.subscribe(subscriber)

        baz.prop_a = "new_value"
        assert len(changes) == 1
        assert changes[0][0] == baz
        assert changes[0][1] == "prop_a"

        baz.prop_c = 100
        assert len(changes) == 2
        assert changes[1][0] == baz
        assert changes[1][1] == "prop_c"

        baz.add_item(5)
        assert baz.prop_d == [1, 2, 3, 5]
        assert len(changes) == 3
        assert changes[2][0] == baz
        assert changes[2][1] == "prop_d"

        baz.f = 60
        assert len(changes) == 4
        assert changes[3][0] == baz
        assert changes[3][1] == "f"

        baz.d = [1, 2, 3]
        assert len(changes) == 5
        assert changes[4][0] == baz
        assert changes[4][1] == "d"

        baz.d.reverse()
        assert len(changes) == 6
        assert changes[5][0] == baz
        assert changes[5][1] == "d"

    def test_repr_shows_version(self):
        """`repr` includes a version that grows with each change."""
        foo = Foo()
        initial_repr = repr(foo)
        assert "version=0" in initial_repr

        foo.prop_a = "value1"
        updated_repr = repr(foo)
        assert "version=1" in updated_repr

        foo.prop_b = "value2"
        updated_repr_2 = repr(foo)
        assert "version=2" in updated_repr_2


class TestObservableList:
    """Notifications from list fields of observable objects."""

    def test_inplace_operators_notify(self):
        """`+=` and `*=` change the list in place and notify once each."""
        changes = []

        def subscriber(sender, field):
            changes.append(field)

        baz = Baz(f=1)
        baz.subscribe(subscriber)

        baz.prop_d += [4]
        assert baz.prop_d == [1, 2, 3, 4]
        assert changes == ["prop_d"]

        baz.prop_d *= 2
        assert baz.prop_d == [1, 2, 3, 4, 1, 2, 3, 4]
        assert changes == ["prop_d", "prop_d"]

    def test_iadd_with_itself(self):
        """`+=` with the list itself appends one copy of its items."""
        baz = Baz(f=1)

        baz.prop_d += baz.prop_d
        assert baz.prop_d == [1, 2, 3, 1, 2, 3]

    def test_extend_with_itself(self):
        """`extend` with the list itself appends its items once, as the same objects."""
        store = Store(items=[[1], 2])
        changes = _watch(store)

        store.items.extend(store.items)
        assert store.items == [[1], 2, [1], 2]
        assert store.items[2] is store.items[0]
        assert changes == ["items"]

    def test_extend_reads_iterable_lazily(self):
        """`extend` appends each item before reading the next one."""
        store = Store(items=[0])

        def gen():
            for _ in range(2):
                yield store.items[-1] + 1

        store.items.extend(gen())
        assert store.items == [0, 1, 2]

    def test_extend_notifies_when_iterable_fails_partway(self):
        """`extend` notifies about items appended before the iterable raised."""
        store = Store(items=[0])
        changes = _watch(store)

        def gen():
            yield 1
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            store.items.extend(gen())
        assert store.items == [0, 1]
        assert changes == ["items"]

    def test_extend_keeps_subscriber_replacement(self):
        """A subscriber that replaces the field during `extend` keeps its value."""
        store = Store(items=[1])
        replaced = []

        def listener(sender, field):
            if not replaced:
                replaced.append(True)
                sender.items = [99]

        store.subscribe(listener)
        store.items.extend([2])
        assert store.items == [99]

    def test_same_child_assignment_is_noop(self):
        """Writing an item's own observable child back to its index doesn't notify."""
        store = Store(items=[[1]])
        store.items[0] = [1]
        changes = _watch(store)

        store.items[0] = store.items[0]
        store.items[-1] = store.items[-1]
        assert changes == []

        store.items[0] = [2]
        store.items[0:1] = store.items[0:1]
        assert changes == ["items", "items"]


class TestObservableDict:
    """Notifications from dict fields of observable objects."""

    def test_assignment_and_item_set_notify(self):
        """Assigning the dict field and setting its keys notify."""
        changes = []

        def subscriber(sender, field):
            changes.append((sender, field))

        qux = Qux()
        qux.subscribe(subscriber)

        qux.prop_e = {"key1": "value1"}
        assert len(changes) == 1
        assert changes[0][0] == qux
        assert changes[0][1] == "prop_e"

        qux.update_key("key2", "value2")
        assert qux.prop_e == {"key1": "value1", "key2": "value2"}
        assert len(changes) == 2
        assert changes[1][0] == qux
        assert changes[1][1] == "prop_e"

        qux.prop_e["key1"] = "updated_value1"
        assert qux.prop_e["key1"] == "updated_value1"
        assert len(changes) == 3
        assert changes[2][0] == qux
        assert changes[2][1] == "prop_e"

    def test_inplace_union_notifies(self):
        """`|=` merges into the dict in place and notifies once."""
        changes = []

        def subscriber(sender, field):
            changes.append(field)

        qux = Qux()
        qux.subscribe(subscriber)

        qux.prop_e |= {"key1": "value1"}
        assert qux.prop_e == {"key1": "value1"}
        assert changes == ["prop_e"]

    @pytest.mark.parametrize(
        "merge",
        [
            lambda d: d.update({"items": []}),
            lambda d: d.update([("items", [])]),
            lambda d: d.update(items=[]),
            lambda d: d.__ior__({"items": []}),
        ],
        ids=["mapping", "pairs", "keywords", "ior"],
    )
    def test_merge_wraps_nested_values(self, merge):
        """Lists merged into the dict notify when they change later."""
        changes = []

        def subscriber(sender, field):
            changes.append(field)

        qux = Qux()
        qux.subscribe(subscriber)

        merge(qux.prop_e)
        changes.clear()
        qux.prop_e["items"].append(1)
        assert qux.prop_e == {"items": [1]}
        assert changes == ["prop_e"]

    def test_update_reads_input_lazily(self):
        """`update` inserts each pair before reading the next one."""
        store = Store()
        changes = _watch(store)

        def pairs():
            for key in ("x", "y"):
                yield key, len(store.mapping)

        store.mapping.update(pairs())
        assert store.mapping == {"x": 0, "y": 1}
        assert changes == ["mapping"]

    def test_update_applies_keywords_last(self):
        """Keyword values override the mapping's values for the same key."""
        store = Store()

        store.mapping.update({"a": 1, "b": 2}, b=3)
        assert store.mapping == {"a": 1, "b": 3}

    def test_update_notifies_when_input_fails_partway(self):
        """`update` notifies about entries inserted before the input raised."""
        store = Store()
        changes = _watch(store)

        with pytest.raises(ValueError):
            store.mapping.update([("a", 1), ("b", 2, 3)])
        assert store.mapping == {"a": 1}
        assert changes == ["mapping"]

    def test_update_rejects_extra_arguments(self):
        """`update` with two positional arguments raises without notifying."""
        store = Store()
        changes = _watch(store)

        with pytest.raises(TypeError):
            store.mapping.update({"a": 1}, {"b": 2})
        assert store.mapping == {}
        assert changes == []

    def test_same_child_assignment_is_noop(self):
        """Writing a key's own observable child back doesn't notify."""
        store = Store()
        store.mapping["items"] = []
        changes = _watch(store)

        store.mapping["items"] = store.mapping["items"]
        assert changes == []

        store.mapping["items"] = []
        assert changes == ["mapping"]


def _iadd_list_in_dict(store):
    store.mapping["list"] += [1]


def _imul_list_in_dict(store):
    store.mapping["list"] *= 2


def _ior_dict_in_dict(store):
    store.mapping["dict"] |= {"a": 1}


def _iadd_list_in_list(store):
    store.items[0] += [1]


def _imul_list_in_list(store):
    store.items[-2] *= 2


def _ior_dict_in_list(store):
    store.items[1] |= {"a": 1}


class TestNestedInplaceOperators:
    """In-place operators on collections nested in observable collections."""

    @pytest.mark.parametrize(
        "op, field, child, expected",
        [
            (_iadd_list_in_dict, "mapping", lambda s: s.mapping["list"], [0, 1]),
            (_imul_list_in_dict, "mapping", lambda s: s.mapping["list"], [0, 0]),
            (_ior_dict_in_dict, "mapping", lambda s: s.mapping["dict"], {"a": 1}),
            (_iadd_list_in_list, "items", lambda s: s.items[0], [0, 1]),
            (_imul_list_in_list, "items", lambda s: s.items[0], [0, 0]),
            (_ior_dict_in_list, "items", lambda s: s.items[1], {"a": 1}),
        ],
        ids=["dict+=", "dict*=", "dict|=", "list+=", "list*=", "list|="],
    )
    def test_notifies_once(self, op, field, child, expected):
        """The nested collection notifies once; writing it back adds nothing."""
        store = Store()
        store.mapping["list"] = [0]
        store.mapping["dict"] = {}
        store.items.extend([[0], {}])
        before = child(store)
        changes = _watch(store)

        op(store)
        assert child(store) is before
        assert child(store) == expected
        assert changes == [field]
