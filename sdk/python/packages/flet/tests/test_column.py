import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Column()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["column"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_alignment_enum():
    r = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND)
    assert isinstance(r.alignment, ft.MainAxisAlignment)
    assert isinstance(r._get_attr("alignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["alignment"] == "spaceAround"


def test_alignment_str():
    r = ft.Column(alignment="center")
    assert isinstance(r.alignment, str)
    assert isinstance(r._get_attr("alignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["alignment"] == "center"


def test_alignment_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Column(alignment="center1")


def test_alignment_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Column(alignment=1)


def test_horizontal_alignment_enum():
    r = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    assert isinstance(r.horizontal_alignment, ft.CrossAxisAlignment)
    assert isinstance(r._get_attr("horizontalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["horizontalalignment"] == "stretch"


def test_horizontal_alignment_str():
    r = ft.Column(horizontal_alignment="center")
    assert isinstance(r.horizontal_alignment, str)
    assert isinstance(r._get_attr("horizontalAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["horizontalalignment"] == "center"


def test_horizontal_alignment_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Column(horizontal_alignment="center1")


def test_horizontal_alignment_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Column(horizontal_alignment=1)


def test_scroll_enum():
    r = ft.Column()
    assert r.scroll is None
    assert r._get_attr("scroll") is None

    r = ft.Column(scroll=ft.ScrollMode.ALWAYS)
    assert isinstance(r.scroll, ft.ScrollMode)
    assert r.scroll == ft.ScrollMode.ALWAYS
    assert r._get_attr("scroll") == "always"

    r = ft.Column(scroll="adaptive")
    assert isinstance(r.scroll, str)
    assert r._get_attr("scroll") == "adaptive"

    r = ft.Column(scroll=True)
    assert isinstance(r.scroll, bool)
    assert r._get_attr("scroll") == "auto"

    r = ft.Column(scroll=False)
    assert isinstance(r.scroll, bool)
    assert r._get_attr("scroll") is None

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Column(scroll="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Column(scroll=1)
