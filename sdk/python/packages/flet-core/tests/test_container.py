import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Container()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=['container'],
            attrs={
                'blendmode': 'modulate',
                'clipbehavior': 'antiAlias',
                'imagefit': 'none',
            },
            commands=[],
        )
    ], 'Test failed'


def test_gradient():
    c = ft.Container(
        gradient=ft.LinearGradient(
            colors=[],
            tile_mode="mirror",
        )
    )
    cmd = c._build_add_commands()
    assert (
        cmd[0].attrs["gradient"]
        == '{"colors":[],"tile_mode":"mirror","begin":{"x":-1,"y":0},"end":{"x":1,"y":0},"type":"linear"}'
    )

    c = ft.Container(
        gradient=ft.LinearGradient(
            colors=[],
            tile_mode=ft.GradientTileMode.REPEATED,
        )
    )
    cmd = c._build_add_commands()
    assert (
        cmd[0].attrs["gradient"]
        == '{"colors":[],"tile_mode":"repeated","begin":{"x":-1,"y":0},"end":{"x":1,"y":0},"type":"linear"}'
    )

    c = ft.Container(
        gradient=ft.LinearGradient(
            colors=[],
        )
    )
    cmd = c._build_add_commands()
    assert (
        cmd[0].attrs["gradient"]
        == '{"colors":[],"tile_mode":"clamp","begin":{"x":-1,"y":0},"end":{"x":1,"y":0},"type":"linear"}'
    )


def test_blend_mode_enum():
    r = ft.Container(blend_mode=ft.BlendMode.LIGHTEN)
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr("blendMode"), str)
    assert r.blend_mode == ft.BlendMode.LIGHTEN
    assert r._get_attr("blendMode") == ft.BlendMode.LIGHTEN.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "lighten"


def test_blend_mode_str():
    r = ft.Container(blend_mode="darken")
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr("blendMode"), str)
    assert r.blend_mode == ft.BlendMode.DARKEN
    assert r._get_attr("blendMode") == ft.BlendMode.DARKEN.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "darken"


def test_clip_behavior_enum():
    r = ft.Container()
    assert r.clip_behavior == ft.ClipBehavior.ANTI_ALIAS
    assert r._get_attr("clipBehavior") == ft.ClipBehavior.ANTI_ALIAS.value

    r = ft.Container(clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert isinstance(r._get_attr("clipBehavior"), str)
    assert r.clip_behavior == ft.ClipBehavior.ANTI_ALIAS
    assert r._get_attr("clipBehavior") == "antiAlias"

    r = ft.Container(clip_behavior="none")
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert isinstance(r._get_attr("clipBehavior"), str)
    assert r.clip_behavior == ft.ClipBehavior.NONE
    assert r._get_attr("clipBehavior") == "none"


def test_image_repeat_enum():
    r = ft.Container()
    assert r.image_repeat is None
    assert r._get_attr("imageRepeat") is None

    r = ft.Container(image_repeat=ft.ImageRepeat.REPEAT)
    assert isinstance(r.image_repeat, ft.ImageRepeat)
    assert r.image_repeat == ft.ImageRepeat.REPEAT
    assert r._get_attr("imageRepeat") == "repeat"

    r = ft.Container(image_repeat="repeatX")
    assert isinstance(r.image_repeat, str)
    assert r._get_attr("imageRepeat") == "repeatX"


def test_image_fit_enum():
    r = ft.Container()
    assert r.image_fit == ft.ImageFit.NONE
    assert r._get_attr('imageFit') == ft.ImageFit.NONE.value

    r = ft.Container(image_fit=ft.ImageFit.FILL)
    assert isinstance(r.image_fit, ft.ImageFit)
    assert isinstance(r._get_attr('imageFit'), str)
    assert r.image_fit == ft.ImageFit.FILL
    assert r._get_attr('imageFit') == 'fill'

    r = ft.Container(image_fit='none')
    assert isinstance(r.image_fit, ft.ImageFit)
    assert isinstance(r._get_attr('imageFit'), str)
    assert r.image_fit == ft.ImageFit.NONE
    assert r._get_attr('imageFit') == 'none'
