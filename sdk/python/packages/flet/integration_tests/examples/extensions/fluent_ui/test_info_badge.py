import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.info_badge.main as info_badge
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
                fluent.InfoBadge("5"),
                fluent.InfoBadge(severity=fluent.InfoBarSeverity.ERROR),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": info_badge.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_info_badge(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "info_badge_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await tester.tap(await tester.find_by_text("Mark all as read"))
    await tester.pump_and_settle()

    assert (await tester.find_by_text("All caught up")).count == 1
    flet_app_function.assert_screenshot(
        "info_badge",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["info_badge_initial", "info_badge"], "info_badge_flow", duration=1000
    )
