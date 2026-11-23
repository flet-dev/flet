import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.toggle_switch.main as toggle_switch
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            intrinsic_width=True,
            controls=[
                fluent.ToggleSwitch(label="Off"),
                fluent.ToggleSwitch(label="On", value=True),
                fluent.ToggleSwitch(label="Disabled", disabled=True),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": toggle_switch.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_toggle_switch(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "toggle_switch_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Wi-Fi")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Wi-Fi is on")).count == 1
    flet_app_function.assert_screenshot(
        "toggle_switch",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["toggle_switch_initial", "toggle_switch"], "toggle_switch_flow", duration=1000
    )
