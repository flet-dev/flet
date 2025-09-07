from dataclasses import dataclass, field

import flet as ft


class Foo(ft.Observable):
    prop_a: str
    prop_b: str


@dataclass
class Bar:
    f: int
    d: list[int] = field(default_factory=list)


@dataclass
class Baz(Bar, ft.Observable):
    prop_c: int = 3
    prop_d: list[int] = field(default_factory=lambda: [1, 2, 3])

    def add_item(self, item: int):
        self.prop_d.append(item)


@dataclass
class Qux(ft.Observable):
    prop_e: dict = field(default_factory=dict)

    def update_key(self, key, value):
        self.prop_e[key] = value


def test_foo_observable():
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


def test_bar_observable():
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


def test_qux_observable():
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


def test_observable_repr():
    foo = Foo()
    initial_repr = repr(foo)
    assert "version=0" in initial_repr

    foo.prop_a = "value1"
    updated_repr = repr(foo)
    assert "version=1" in updated_repr

    foo.prop_b = "value2"
    updated_repr_2 = repr(foo)
    assert "version=2" in updated_repr_2
