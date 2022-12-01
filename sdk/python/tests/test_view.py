import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.View()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["view"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_horizontal_alignment_enum():
    r = ft.View(horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    assert isinstance(r.horizontal_alignment, ft.CrossAxisAlignment)
    assert isinstance(r._get_attr("horizontalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["horizontalalignment"] == "stretch"


def test_horizontal_alignment_str():
    r = ft.View(horizontal_alignment="center")
    assert isinstance(r.horizontal_alignment, str)
    assert isinstance(r._get_attr("horizontalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["horizontalalignment"] == "center"


def test_horizontal_alignment_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.View(horizontal_alignment="center1")


def test_horizontal_alignment_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.View(horizontal_alignment=1)


def test_vertical_alignment_enum():
    r = ft.View(vertical_alignment=ft.MainAxisAlignment.CENTER)
    assert isinstance(r.vertical_alignment, ft.MainAxisAlignment)
    assert isinstance(r._get_attr("verticalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["verticalalignment"] == "center"


def test_vertical_alignment_str():
    r = ft.View(vertical_alignment="center")
    assert isinstance(r.vertical_alignment, str)
    assert isinstance(r._get_attr("verticalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["verticalalignment"] == "center"


def test_vertical_alignment_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.View(vertical_alignment="center1")


def test_vertical_alignment_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.View(vertical_alignment=1)


def test_scroll_enum():
    r = ft.View()
    assert r.scroll is None
    assert r._get_attr("scroll") is None

    r = ft.View(scroll=ft.ScrollMode.ALWAYS)
    assert isinstance(r.scroll, ft.ScrollMode)
    assert r.scroll == ft.ScrollMode.ALWAYS
    assert r._get_attr("scroll") == "always"

    r = ft.View(scroll="adaptive")
    assert isinstance(r.scroll, str)
    assert r._get_attr("scroll") == "adaptive"

    r = ft.View(scroll=True)
    assert isinstance(r.scroll, bool)
    assert r._get_attr("scroll") == "auto"

    r = ft.View(scroll=False)
    assert isinstance(r.scroll, bool)
    assert r._get_attr("scroll") is None

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.View(scroll="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.View(scroll=1)
