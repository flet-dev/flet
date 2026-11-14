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
        """`extend` with the list itself appends one copy of its items."""
        baz = Baz(f=1)

        baz.prop_d.extend(baz.prop_d)
        assert baz.prop_d == [1, 2, 3, 1, 2, 3]


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
