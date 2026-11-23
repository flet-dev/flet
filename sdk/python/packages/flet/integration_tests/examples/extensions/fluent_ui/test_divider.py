import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.divider.main as divider
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=200, controls=[ft.Text("Above"), fluent.Divider(), ft.Text("Below")]
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": divider.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_divider(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await tester.pump_and_settle()

    assert (await tester.find_by_text("Privacy")).count == 1
    flet_app_function.assert_screenshot(
        "divider",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
