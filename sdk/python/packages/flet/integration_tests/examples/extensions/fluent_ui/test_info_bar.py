import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.info_bar.main as info_bar
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=360,
            controls=[
                fluent.InfoBar(title="Info", content="A neutral message."),
                fluent.InfoBar(
                    title="Success",
                    content="It worked.",
                    severity=fluent.InfoBarSeverity.SUCCESS,
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": info_bar.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_info_bar(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Sync failed")).count == 1
    flet_app_function.assert_screenshot(
        "info_bar",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
