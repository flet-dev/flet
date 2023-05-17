import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_image_add():
    i = ft.Image(
        src='https://www.w3schools.com/css/img_5terre.jpg',
    )
    assert isinstance(i, ft.Control)
    assert isinstance(i, ft.Image)
    assert i._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=['image'],
            attrs={
                'colorblendmode': 'modulate',
                'fit': 'none',
                'repeat': 'noRepeat',
                'src': 'https://www.w3schools.com/css/img_5terre.jpg',
            },
            commands=[],
        )
    ], 'Test failed'


def test_color_blend_mode_enum():
    r = ft.Image(color_blend_mode=ft.BlendMode.LIGHTEN)
    assert isinstance(r.color_blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr('colorBlendMode'), str)
    assert r.color_blend_mode == ft.BlendMode.LIGHTEN
    assert r._get_attr('colorBlendMode') == ft.BlendMode.LIGHTEN.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs['colorblendmode'] == 'lighten'


def test_color_blend_mode_str():
    r = ft.Image(color_blend_mode='darken')
    assert isinstance(r.color_blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr('colorBlendMode'), str)
    assert r.color_blend_mode == ft.BlendMode.DARKEN
    assert r._get_attr('colorBlendMode') == ft.BlendMode.DARKEN.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs['colorblendmode'] == 'darken'


def test_repeat_enum():
    r = ft.Image()
    assert r.repeat == ft.ImageRepeat.NO_REPEAT
    assert r._get_attr('repeat') == ft.ImageRepeat.NO_REPEAT.value

    r = ft.Image(repeat=ft.ImageRepeat.REPEAT)
    assert isinstance(r.repeat, ft.ImageRepeat)
    assert isinstance(r._get_attr('repeat'), str)
    assert r.repeat == ft.ImageRepeat.REPEAT
    assert r._get_attr('repeat') == 'repeat'

    r = ft.Image(repeat='repeatX')
    assert isinstance(r.repeat, ft.ImageRepeat)
    assert isinstance(r._get_attr('repeat'), str)
    assert r.repeat == ft.ImageRepeat.REPEAT_X
    assert r._get_attr('repeat') == 'repeatX'


def test_fit_enum():
    r = ft.Image()
    assert r.fit == ft.ImageFit.NONE
    assert r._get_attr('fit') == ft.ImageFit.NONE.value

    r = ft.Image(fit=ft.ImageFit.FILL)
    assert isinstance(r.fit, ft.ImageFit)
    assert isinstance(r._get_attr('fit'), str)
    assert r.fit == ft.ImageFit.FILL
    assert r._get_attr('fit') == 'fill'

    r = ft.Image(fit='none')
    assert isinstance(r.fit, ft.ImageFit)
    assert isinstance(r._get_attr('fit'), str)
    assert r.fit == ft.ImageFit.NONE
    assert r._get_attr('fit') == 'none'
