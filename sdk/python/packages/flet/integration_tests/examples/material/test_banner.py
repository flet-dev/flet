import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    await flet_app_function.resize_page(400, 200)
    banner = ft.Banner(
        leading=ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.PRIMARY),
        content=ft.Text("Backup completed successfully."),
        actions=[ft.TextButton("Dismiss")],
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        open=True,
    )
    page.add(banner)
    page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    page.update()
