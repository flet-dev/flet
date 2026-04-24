import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.banner.basic import main as basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    flet_app_function.resize_page(400, 200)
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


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic_banner_flow(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    show_banner_button = await flet_app_function.tester.find_by_text("Show Banner")
    await flet_app_function.tester.mouse_hover(show_banner_button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "hover_show_banner",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.tap(show_banner_button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "banner_open",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    ignore_button = await flet_app_function.tester.find_by_text("Ignore")
    await flet_app_function.tester.mouse_hover(ignore_button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "hover_ignore",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.tap(ignore_button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "after_ignore",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "before_click",
            "hover_show_banner",
            "banner_open",
            "hover_ignore",
            "after_ignore",
        ],
        "banner_flow",
        duration=1000,
    )
