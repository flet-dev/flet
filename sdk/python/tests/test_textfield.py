import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.TextField()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["textfield"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_text_align_enum():
    r = ft.TextField(text_align=ft.TextAlign.LEFT)
    assert isinstance(r.text_align, ft.TextAlign)
    assert isinstance(r._get_attr("textAlign"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["textalign"] == "left"


def test_text_align_str():
    r = ft.TextField(text_align="left")
    assert isinstance(r.text_align, str)
    assert isinstance(r._get_attr("textAlign"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["textalign"] == "left"


def test_text_align_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(text_align="center1")


def test_text_align_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(text_align=1)


def test_keyboard_type_enum():
    r = ft.TextField()
    assert r.keyboard_type is None
    assert r._get_attr("keyboardType") is None

    r = ft.TextField(keyboard_type=ft.KeyboardType.NONE)
    assert isinstance(r.keyboard_type, ft.KeyboardType)
    assert r.keyboard_type == ft.KeyboardType.NONE
    assert r._get_attr("keyboardType") == "none"

    r = ft.TextField(keyboard_type="phone")
    assert isinstance(r.keyboard_type, str)
    assert r._get_attr("keyboardType") == "phone"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(keyboard_type="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(keyboard_type=1)


def test_capitalization_enum():
    r = ft.TextField()
    assert r.capitalization == ft.TextCapitalization.NONE
    assert r._get_attr("capitalization") is None

    r = ft.TextField(capitalization=ft.TextCapitalization.WORDS)
    assert isinstance(r.capitalization, ft.TextCapitalization)
    assert r.capitalization == ft.TextCapitalization.WORDS
    assert r._get_attr("capitalization") == "words"

    r = ft.TextField(capitalization="sentences")
    assert isinstance(r.capitalization, str)
    assert r._get_attr("capitalization") == "sentences"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(capitalization="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(capitalization=1)


def test_border_enum():
    r = ft.TextField()
    assert r.border is None
    assert r._get_attr("border") is None

    r = ft.TextField(border=ft.InputBorder.OUTLINE)
    assert isinstance(r.border, ft.InputBorder)
    assert r.border == ft.InputBorder.OUTLINE
    assert r._get_attr("border") == "outline"

    r = ft.TextField(border="none")
    assert isinstance(r.border, str)
    assert r._get_attr("border") == "none"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(border="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.TextField(border=1)
