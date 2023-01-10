import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Dropdown()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["dropdown"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_border_enum():
    r = ft.Dropdown()
    assert r.border is None
    assert r._get_attr("border") is None

    r = ft.Dropdown(border=ft.InputBorder.OUTLINE)
    assert isinstance(r.border, ft.InputBorder)
    assert r.border == ft.InputBorder.OUTLINE
    assert r._get_attr("border") == "outline"

    r = ft.Dropdown(border="none")
    assert isinstance(r.border, str)
    assert r._get_attr("border") == "none"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Dropdown(border="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Dropdown(border=1)
