import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.info_label.main as info_label
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=260,
            controls=[
                fluent.InfoLabel(
                    label="Email",
                    content=fluent.TextBox(placeholder="name@example.com"),
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": info_label.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_info_label(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await tester.pump_and_settle()

    assert (await tester.find_by_text("Subscribe to the newsletter")).count == 1
    flet_app_function.assert_screenshot(
        "info_label",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
