import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.icon_button.main as icon_button
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Row(
            tight=True,
            controls=[
                fluent.IconButton(fluent.FluentIcons.SETTINGS),
                fluent.IconButton(fluent.FluentIcons.SETTINGS, disabled=True),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": icon_button.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_icon_button(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "icon_button_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("favorite")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text("Added to favorites")
    ).count == 1
    flet_app_function.assert_screenshot(
        "icon_button",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["icon_button_initial", "icon_button"], "icon_button_flow", duration=1000
    )
