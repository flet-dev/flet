import asyncio

import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.responsive_row import basic, custom_breakpoint


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ResponsiveRow(
            controls=[
                ft.Button(
                    f"Button {i}",
                    color=ft.Colors.BLUE_GREY_300,
                    col={
                        ft.ResponsiveRowBreakpoint.XS: 12,
                        ft.ResponsiveRowBreakpoint.MD: 6,
                        ft.ResponsiveRowBreakpoint.LG: 3,
                    },
                )
                for i in range(1, 6)
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(1000, 500)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
            delay=ft.Duration(seconds=1),
        ),
    )
    flet_app_function.resize_page(800, 500)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
            delay=ft.Duration(seconds=1),
        ),
    )
    flet_app_function.resize_page(200, 500)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic_3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
            delay=ft.Duration(seconds=1),
        ),
    )
    flet_app_function.create_gif(
        ["basic_1", "basic_2", "basic_3"],
        "basic",
        duration=1600,
        disposal=ftt.DisposalMode.BACKGROUND,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_breakpoint.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_breakpoint(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(800, 600)
    flet_app_function.page.update()
    await asyncio.sleep(1)
    for _ in range(10):
        await flet_app_function.tester.pump(100)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "custom_breakpoint_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.resize_page(650, 600)
    flet_app_function.page.update()
    for _ in range(10):
        await flet_app_function.tester.pump(100)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "custom_breakpoint_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.resize_page(300, 600)
    flet_app_function.page.update()
    for _ in range(10):
        await flet_app_function.tester.pump(100)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "custom_breakpoint_3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["custom_breakpoint_1", "custom_breakpoint_2", "custom_breakpoint_3"],
        "custom_breakpoint",
        duration=1600,
        disposal=ftt.DisposalMode.BACKGROUND,
    )
