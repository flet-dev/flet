import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.shader_mask import (
    pink_radial_glow,
    linear_and_radial_gradients,
    fade_out_image_bottom,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    sm = ft.ShaderMask(
        blend_mode=ft.BlendMode.MULTIPLY,
        shader=ft.LinearGradient(
            begin=ft.Alignment.CENTER_LEFT,
            end=ft.Alignment.CENTER_RIGHT,
            colors=[ft.Colors.WHITE, ft.Colors.BLACK],
            tile_mode=ft.GradientTileMode.CLAMP,
        ),
        content=ft.Image(
            src="https://picsum.photos/id/288/300/300",
            height=300,
            fit=ft.BoxFit.FILL,
        ),
    )
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.window.width = 300
    flet_app_function.page.window.height = 350
    flet_app_function.page.add(sm)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(duration=ft.Duration(seconds=3))
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": pink_radial_glow.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_pink_radial_glow(flet_app_function: ftt.FletTestApp):
    await flet_app_function.tester.pump_and_settle(duration=ft.Duration(seconds=3))
    flet_app_function.assert_screenshot(
        "pink_radial_glow",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": linear_and_radial_gradients.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_linear_and_radial_gradients(flet_app_function: ftt.FletTestApp):
    await flet_app_function.tester.pump_and_settle(duration=ft.Duration(seconds=3))
    flet_app_function.assert_screenshot(
        "linear_and_radial_gradients",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": fade_out_image_bottom.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_fade_out_image_bottom(flet_app_function: ftt.FletTestApp):
    await flet_app_function.tester.pump_and_settle(duration=ft.Duration(seconds=3))
    flet_app_function.assert_screenshot(
        "fade_out_image_bottom",
        await flet_app_function.take_page_controls_screenshot(),
    )
