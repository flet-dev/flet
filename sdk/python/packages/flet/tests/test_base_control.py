import sys
import typing

import pytest

import flet as ft
from flet.controls.base_control import control


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


@pytest.mark.skipif(
    sys.version_info < (3, 11), reason="typing.get_overloads requires Python 3.11+"
)
def test_control_args_overload_accepts_only_str_name():
    """
    `@control("Name")` must not match a `type[T]` parameter: T would stay
    unbound and mypy would infer the returned decorator as `type[Never]`.
    """
    _, with_args = typing.get_overloads(control)
    hints = typing.get_type_hints(with_args)
    assert hints["dart_widget_name"] == typing.Optional[str]
