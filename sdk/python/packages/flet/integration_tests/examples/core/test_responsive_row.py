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
    flet_app_function.assert_screenshot(
        "responsive1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
            delay=ft.Duration(seconds=1),
        ),
    )
    flet_app_function.resize_page(800, 500)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "responsive2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
            delay=ft.Duration(seconds=1),
        ),
    )
    flet_app_function.resize_page(200, 500)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "responsive3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
            delay=ft.Duration(seconds=1),
        ),
    )
    flet_app_function.create_gif(
        ["responsive1", "responsive2", "responsive3"],
        "responsive_row_basic",
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
    flet_app_function.resize_page(1000, 800)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "responsive_custom_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.resize_page(650, 800)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "responsive_custom_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.resize_page(200, 800)
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "responsive_custom_3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["responsive_custom_1", "responsive_custom_2", "responsive_custom_3"],
        "responsive_row_custom_breakpoint",
        duration=1600,
        disposal=ftt.DisposalMode.BACKGROUND,
    )
