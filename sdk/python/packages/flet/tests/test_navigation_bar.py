import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.NavigationBar()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["navigationbar"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_extension_set_enum():
    r = ft.NavigationBar()
    assert r.label_behavior is None
    assert r._get_attr("labelType") is None

    r = ft.NavigationBar(label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW)
    assert isinstance(r.label_behavior, ft.NavigationBarLabelBehavior)
    assert r.label_behavior == ft.NavigationBarLabelBehavior.ALWAYS_SHOW
    assert r._get_attr("labelType") == "alwaysShow"

    r = ft.NavigationBar(label_behavior="alwaysHide")
    assert isinstance(r.label_behavior, str)
    assert r._get_attr("labelType") == "alwaysHide"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.NavigationBar(label_behavior="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.NavigationBar(label_behavior=1)
