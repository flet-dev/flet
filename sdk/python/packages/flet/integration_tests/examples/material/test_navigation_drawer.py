import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.navigation_drawer import position_end, position_start


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    nvd = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(label="Item 1"),
            ft.NavigationDrawerDestination(label="Item 2"),
            ft.NavigationDrawerDestination(label="Item 3"),
        ],
        tile_padding=ft.Padding(top=10),
    )
    flet_app_function.resize_page(400, 400)
    flet_app_function.page.drawer = nvd
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=800)
    )
    await flet_app_function.page.show_drawer()
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=800)
    )
    flet_app_function.assert_screenshot(
        "image_for_docs",
        await flet_app_function.page.take_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": position_end.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_position_end(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "position_end1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    btn = await flet_app_function.tester.find_by_text_containing("Show")
    await flet_app_function.tester.mouse_hover(btn)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "position_end2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(btn)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "position_end3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["position_end1", "position_end2", "position_end3"],
        "position_end",
        duration=1600,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": position_start.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_position_start(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "position_start1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    btn = await flet_app_function.tester.find_by_text_containing("Show")
    await flet_app_function.tester.mouse_hover(btn)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "position_start2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(btn)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "position_start3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["position_start1", "position_start2", "position_start3"],
        "position_start",
        duration=1600,
    )
