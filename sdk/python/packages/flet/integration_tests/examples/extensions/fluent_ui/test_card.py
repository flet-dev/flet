import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.card.main as card
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=fluent.Card(
            width=240,
            content=ft.Text("Content inside a card"),
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": card.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_card(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Manage storage")).count == 1
    flet_app_function.assert_screenshot(
        "card",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
