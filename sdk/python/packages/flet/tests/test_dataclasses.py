from dataclasses import dataclass, field, fields


@dataclass
class Foo:
    prop_a: str = "default_a"
    prop_b: str = field(default="default_b")


def test_default_values():
    foo = Foo()
    assert foo.prop_a == "default_a"

    foo_fields = fields(foo)
    assert len(foo_fields) == 2
    assert foo_fields[0].default == "default_a"
    assert foo_fields[1].default == "default_b"


def test_equality():
    foo1 = Foo()
    foo2 = Foo()
    assert foo1 == foo2
