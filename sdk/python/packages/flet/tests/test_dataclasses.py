from dataclasses import dataclass, field, fields


@dataclass
class Foo:
    prop_a: str = "default_a"
    prop_b: str = field(default="default_b")


class Bar:
    prop_a: str = "default_a"
    prop_b: str = "default_b"


class Baz:
    prop_a: str = "default_a"
    prop_b: str = "default_b"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Baz):
            return NotImplemented
        return self.prop_a == value.prop_a and self.prop_b == value.prop_b


def test_default_values():
    foo = Foo()
    assert foo.prop_a == "default_a"

    foo_fields = fields(foo)
    assert len(foo_fields) == 2
    assert foo_fields[0].default == "default_a"
    assert foo_fields[1].default == "default_b"


def test_equality_default():
    foo1 = Foo()
    foo2 = Foo()
    assert foo1 == foo2


def test_equality_with_props():
    foo1 = Foo(prop_a="custom_a", prop_b="custom_b")
    foo2 = Foo(prop_a="custom_a", prop_b="custom_b")
    assert foo1 == foo2


def test_equality_regular_classes():
    bar1 = Bar()
    bar2 = Bar()
    assert bar1 != bar2


def test_equality_with_eq_method():
    baz1 = Baz()
    baz2 = Baz()
    assert baz1 == baz2


def test_lists_equality():
    foo1 = Foo(prop_a="a", prop_b="b")
    foo2 = Foo(prop_a="a", prop_b="b")
    foo_list1 = [foo1]
    foo_list2 = [foo2]
    assert foo_list1 == foo_list2

    bar1 = Bar()
    bar2 = Bar()
    bar_list1 = [bar1]
    bar_list2 = [bar2]
    assert bar_list1 != bar_list2

    baz1 = Baz()
    baz2 = Baz()
    baz_list1 = [foo1, baz1]
    baz_list2 = [foo2, baz2]
    assert baz_list1 == baz_list2
