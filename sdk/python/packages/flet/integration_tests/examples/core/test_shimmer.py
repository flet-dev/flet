import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    flet_app_function.resize_page(400, 400)
    page.update()
    await flet_app_function.tester.pump_and_settle()
    page.add(
        ft.Shimmer(
            base_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
            highlight_color=ft.Colors.WHITE,
            content=ft.Column(
                controls=[
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                ],
            ),
        )
    )
    await flet_app_function.tester.pump(1000)
    await flet_app_function.tester.pump(800)
    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
