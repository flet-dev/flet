import flet_core as ft
import pytest
from flet_core.protocol import Command


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
    assert r.border == ft.InputBorder.OUTLINE
    assert isinstance(r.border, ft.BlendMode)
    assert isinstance(r._get_attr('border'), str)
    assert r.border == ft.InputBorder.OUTLINE
    assert r._get_attr('border') == ft.InputBorder.OUTLINE.value

    r = ft.Dropdown(border=ft.InputBorder.NONE)
    assert isinstance(r.border, ft.BlendMode)
    assert isinstance(r._get_attr('border'), str)
    assert r.border == ft.InputBorder.NONE
    assert r._get_attr('border') == ft.InputBorder.NONE.value
    assert r._get_attr("border") == "none"
