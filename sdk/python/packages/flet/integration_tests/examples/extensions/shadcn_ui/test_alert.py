import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.alert.main as alert
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Alert(
            width=360,
            icon=shad.LucideIcons.TERMINAL,
            title="Heads up!",
            description="You can add components using the CLI.",
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": alert.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_alert(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Heads up!")).count == 1
    flet_app_function.assert_screenshot(
        "alert",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
