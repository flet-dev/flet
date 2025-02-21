from flet.core.protocol import Command

import flet as ft


def test_instance_no_attrs_set():
    r = ft.Container()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["container"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_gradient():
    c = ft.Container(
        gradient=ft.LinearGradient(
            colors=[],
            tile_mode=ft.GradientTileMode.MIRROR,
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
    r = ft.Container(blend_mode=ft.BlendMode.LIGHTEN, bgcolor=ft.Colors.RED)
    assert isinstance(r.blend_mode, ft.BlendMode)
    assert isinstance(r._get_attr("blendMode"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["blendmode"] == "lighten"


def test_clip_behavior_enum():
    r = ft.Container()
    assert r.clip_behavior is None
    assert r._get_attr("clipBehavior") is None

    r = ft.Container(clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert r.clip_behavior == ft.ClipBehavior.ANTI_ALIAS
    assert r._get_attr("clipBehavior") == "antiAlias"

    r = ft.Container(clip_behavior=ft.ClipBehavior.NONE)
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert r._get_attr("clipBehavior") == "none"


def test_image_repeat_enum():
    r = ft.Container()
    assert r.image is None

    r = ft.Container(image=ft.DecorationImage(repeat=ft.ImageRepeat.REPEAT))
    assert isinstance(r.image.repeat, ft.ImageRepeat)
    assert r.image.repeat == ft.ImageRepeat.REPEAT


def test_image_fit_enum():
    r = ft.Container()
    assert r.image is None

    r = ft.Container(image=ft.DecorationImage(fit=ft.ImageFit.FILL))
    assert isinstance(r.image.fit, ft.ImageFit)
    assert r.image.fit == ft.ImageFit.FILL
