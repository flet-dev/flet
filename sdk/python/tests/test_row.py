import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Row()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["row"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_alignment_enum():
    r = ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND)
    assert isinstance(r.alignment, ft.MainAxisAlignment)
    assert isinstance(r._get_attr("alignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["alignment"] == "spaceAround"


def test_alignment_str():
    r = ft.Row(alignment="center")
    assert isinstance(r.alignment, str)
    assert isinstance(r._get_attr("alignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["alignment"] == "center"


def test_alignment_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Row(alignment="center1")


def test_alignment_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Row(alignment=1)


def test_vertical_alignment_enum():
    r = ft.Row(vertical_alignment=ft.CrossAxisAlignment.STRETCH)
    assert isinstance(r.vertical_alignment, ft.CrossAxisAlignment)
    assert isinstance(r._get_attr("verticalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["verticalalignment"] == "stretch"


def test_vertical_alignment_str():
    r = ft.Row(vertical_alignment="center")
    assert isinstance(r.vertical_alignment, str)
    assert isinstance(r._get_attr("verticalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["verticalalignment"] == "center"


def test_vertical_alignment_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Row(vertical_alignment="center1")


def test_vertical_alignment_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Row(vertical_alignment=1)


def test_scroll_enum():
    r = ft.Row()
    assert r.scroll is None
    assert r._get_attr("scroll") is None

    r = ft.Row(scroll=ft.ScrollMode.ALWAYS)
    assert isinstance(r.scroll, ft.ScrollMode)
    assert r.scroll == ft.ScrollMode.ALWAYS
    assert r._get_attr("scroll") == "always"

    r = ft.Row(scroll="adaptive")
    assert isinstance(r.scroll, str)
    assert r._get_attr("scroll") == "adaptive"

    r = ft.Row(scroll=True)
    assert isinstance(r.scroll, bool)
    assert r._get_attr("scroll") == "auto"

    r = ft.Row(scroll=False)
    assert isinstance(r.scroll, bool)
    assert r._get_attr("scroll") is None

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Row(scroll="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Row(scroll=1)
