import dataclasses

import flet as ft
from flet.controls.base_control import control
from flet.controls.value_types import value


def test_controls_equality():
    t1 = ft.Text("A")
    t2 = ft.Text("A")
    assert t1 == t2

    t3 = ft.Text("B", data=1)
    t4 = ft.Text("B", data=2)
    assert t3 != t4

    c1 = ft.Column(
        [ft.Text("Some text"), ft.Button("Some button")], expand=True, data=1
    )
    c2 = ft.Column(
        [ft.Text("Some text"), ft.Button("Some button")], expand=True, data=1
    )
    assert c1 == c2


def test_keys():
    k1 = ft.ValueKey(1)
    assert str(k1) == "1"
    assert k1._type == "value"

    k2 = ft.ScrollKey("section_a")
    assert str(k2) == "section_a"
    assert k2._type == "scroll"

    t1 = ft.Text("A", key=ft.ValueKey("1"))
    t2 = ft.Text("A", key=ft.ValueKey("1"))
    assert t1 == t2


def test_dataclass_transforms_declare_field_specifiers():
    # Type checkers only honor `dataclasses.field()` arguments (e.g. `init=False`)
    # on `@control` and `@value` classes when `field` is a declared field specifier.
    for decorator in (control, value):
        transform = decorator.__dataclass_transform__
        assert dataclasses.field in transform["field_specifiers"]
