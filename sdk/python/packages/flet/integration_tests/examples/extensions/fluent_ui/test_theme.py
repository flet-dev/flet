import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.theme.main as theme
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=fluent.Theme(
            accent_color=ft.Colors.PURPLE, content=fluent.FilledButton("Themed")
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": theme.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Continue")).count == 3
    flet_app_function.assert_screenshot(
        "theme",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
