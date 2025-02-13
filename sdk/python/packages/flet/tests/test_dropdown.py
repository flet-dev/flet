import flet as ft
from flet.core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.DropdownOld()
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
    r = ft.DropdownOld()
    assert r.border is None
    assert r._get_attr("border") is None

    r = ft.DropdownOld(border=ft.InputBorder.OUTLINE)
    assert isinstance(r.border, ft.InputBorder)
    assert r.border == ft.InputBorder.OUTLINE
    assert r._get_attr("border") == "outline"

    r = ft.DropdownOld(border="none")
    assert isinstance(r.border, str)
    assert r._get_attr("border") == "none"
