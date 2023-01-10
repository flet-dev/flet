import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.ShaderMask()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["shadermask"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_blend_mode_enum():
    r = ft.ShaderMask(blend_mode=ft.BlendMode.LIGHTEN)
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr("blendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "lighten"


def test_blend_mode_str():
    r = ft.ShaderMask(blend_mode="darken")
    assert isinstance(r.blend_mode, str)
    assert isinstance(r._get_attr("blendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "darken"


def test_blend_mode_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.ShaderMask(blend_mode="center1")


def test_blend_mode_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.ShaderMask(blend_mode=1)
