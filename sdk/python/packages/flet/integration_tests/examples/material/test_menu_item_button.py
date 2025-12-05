import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.menu_item_button import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Row(
            controls=[
                ft.MenuItemButton(
                    content=ft.Text("Yes"),
                    on_click=lambda e: print("yes"),
                    autofocus=True,
                ),
                ft.MenuItemButton(
                    content=ft.Text("No"),
                    on_click=lambda e: print("no"),
                ),
                ft.MenuItemButton(
                    content=ft.Text("Maybe"),
                    on_click=lambda e: print("maybe"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            height=50,
            width=200,
            expand=True,
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
    flet_app_function.resize_page(400, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "basic1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    btn = await flet_app_function.tester.find_by_text("BgColors")
    await flet_app_function.tester.tap(btn)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    mib = await flet_app_function.tester.find_by_text("Green")
    await flet_app_function.tester.tap(mib)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["basic1", "basic2", "basic3"],
        "basic",
        duration=1600,
    )
