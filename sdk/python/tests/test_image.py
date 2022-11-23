import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_image_add():
    i = ft.Image(
        src="https://www.w3schools.com/css/img_5terre.jpg",
    )
    assert isinstance(i, ft.Control)
    assert isinstance(i, ft.Image)
    assert i._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["image"],
            attrs={
                "src": "https://www.w3schools.com/css/img_5terre.jpg",
            },
            commands=[],
        )
    ], "Test failed"


def test_color_blend_mode_enum():
    r = ft.Image(color_blend_mode=ft.BlendMode.LIGHTEN)
    assert isinstance(r.color_blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr("colorBlendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["colorblendmode"] == "lighten"


def test_color_blend_mode_str():
    r = ft.Image(color_blend_mode="darken")
    assert isinstance(r.color_blend_mode, str)
    assert isinstance(r._get_attr("colorBlendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["colorblendmode"] == "darken"


def test_color_blend_mode_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Image(color_blend_mode="center1")


def test_color_blend_mode_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Image(color_blend_mode=1)
