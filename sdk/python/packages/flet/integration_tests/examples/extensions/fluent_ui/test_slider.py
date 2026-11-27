import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.slider.main as slider
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(width=240, controls=[fluent.Slider(value=40)]),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": slider.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_slider(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "slider_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    # Tapping the middle of the track moves the thumb there.
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("volume")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Volume: 50")).count == 1
    flet_app_function.assert_screenshot(
        "slider",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["slider_initial", "slider"], "slider_flow", duration=1000
    )
