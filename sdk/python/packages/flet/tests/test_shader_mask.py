import flet as ft
from flet.core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.ShaderMask(shader=ft.LinearGradient(colors=[ft.Colors.BLUE]))
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["shadermask"],
            attrs={
                "shader": '{"colors":["blue"],"tile_mode":"clamp","begin":{"x":-1,"y":0},"end":{"x":1,"y":0},"type":"linear"}'
            },
            commands=[],
        )
    ], "Test failed"


def test_blend_mode_enum():
    r = ft.ShaderMask(
        shader=ft.LinearGradient(colors=[ft.Colors.BLUE]),
        blend_mode=ft.BlendMode.LIGHTEN,
    )
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr("blendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "lighten"


def test_blend_mode_str():
    r = ft.ShaderMask(
        shader=ft.LinearGradient(colors=[ft.Colors.BLUE]), blend_mode="darken"
    )
    assert isinstance(r.blend_mode, str)
    assert isinstance(r._get_attr("blendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "darken"
