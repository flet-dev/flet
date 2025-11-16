import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.bottom_sheet import basic, fullscreen


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(200, 200)
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT

    sheet = ft.BottomSheet(
        content=ft.Column(
            width=150,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Choose an option"),
                ft.TextButton("Dismiss"),
            ],
        )
    )
    flet_app_function.page.show_dialog(sheet)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
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
    flet_app_function.resize_page(350, 450)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # open bottom sheet
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Display bottom sheet")
    )
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # create gif
    flet_app_function.create_gif(
        [f"basic_{i}" for i in range(1, 3)],
        output_name="basic",
        duration=2000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": fullscreen.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_fullscreen(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 450)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "fullscreen_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # open bottom sheet
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Display bottom sheet")
    )
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "fullscreen_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # close bottom sheet
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Close bottom sheet")
    )
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "fullscreen_3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # toggle switch
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Fullscreen")
    )
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "fullscreen_4",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # open bottom sheet
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Display bottom sheet")
    )
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "fullscreen_5",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # create gif
    flet_app_function.create_gif(
        [f"fullscreen_{i}" for i in range(1, 6)],
        output_name="fullscreen",
        duration=2000,
    )
