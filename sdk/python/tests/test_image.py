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


def test_repeat_enum():
    r = ft.Image()
    assert r.repeat is None
    assert r._get_attr("repeat") is None

    r = ft.Image(repeat=ft.ImageRepeat.REPEAT)
    assert isinstance(r.repeat, ft.ImageRepeat)
    assert r.repeat == ft.ImageRepeat.REPEAT
    assert r._get_attr("repeat") == "repeat"

    r = ft.Image(repeat="repeatX")
    assert isinstance(r.repeat, str)
    assert r._get_attr("repeat") == "repeatX"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Image(repeat="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Image(repeat=1)


def test_fit_enum():
    r = ft.Image()
    assert r.fit is None
    assert r._get_attr("fit") is None

    r = ft.Image(fit=ft.ImageFit.FILL)
    assert isinstance(r.fit, ft.ImageFit)
    assert r.fit == ft.ImageFit.FILL
    assert r._get_attr("fit") == "fill"

    r = ft.Image(fit="none")
    assert isinstance(r.fit, str)
    assert r._get_attr("fit") == "none"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Image(fit="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Image(fit=1)
