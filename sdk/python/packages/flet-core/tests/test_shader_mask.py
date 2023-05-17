import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.ShaderMask()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=['shadermask'],
            attrs={'blendmode': 'modulate'},
            commands=[],
        )
    ], 'Test failed'


def test_blend_mode_enum():
    r = ft.ShaderMask(blend_mode=ft.BlendMode.LIGHTEN)
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr('blendMode'), str)
    assert r.color_blend_mode == ft.BlendMode.LIGHTEN
    assert r._get_attr("blendMode") == ft.BlendMode.LIGHTEN.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs['blendmode'] == 'lighten'


def test_blend_mode_str():
    r = ft.ShaderMask(blend_mode='darken')
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr('blendMode'), str)
    assert r.color_blend_mode == ft.BlendMode.DARKEN
    assert r._get_attr("blendMode") == ft.BlendMode.DARKEN.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs['blendmode'] == 'darken'
