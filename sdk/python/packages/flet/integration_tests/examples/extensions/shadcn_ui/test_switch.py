import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.switch.main as switch
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
                shad.Switch(label="Off"),
                shad.Switch(label="On", value=True),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": switch.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_switch(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "switch_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Airplane mode")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text("Airplane mode is on")
    ).count == 1
    flet_app_function.assert_screenshot(
        "switch",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["switch_initial", "switch"], "switch_flow", duration=1000
    )
