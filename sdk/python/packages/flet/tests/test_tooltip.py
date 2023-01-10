import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Tooltip()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["tooltip"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_text_align_enum():
    r = ft.Tooltip()
    assert r.text_align == ft.TextAlign.NONE
    assert r._get_attr("textAlign") is None

    r = ft.Tooltip(text_align=ft.TextAlign.RIGHT)
    assert isinstance(r.text_align, ft.TextAlign)
    assert r.text_align == ft.TextAlign.RIGHT
    assert r._get_attr("textAlign") == "right"

    r = ft.Tooltip(text_align="left")
    assert isinstance(r.text_align, str)
    assert r._get_attr("textAlign") == "left"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Tooltip(text_align="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Tooltip(text_align=1)
