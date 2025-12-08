import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.menu_bar import nested_submenus


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(100, 200)
    flet_app_function.page.update()
    mb = ft.MenuBar(
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Submenu"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("Item 1")),
                    ft.MenuItemButton(content=ft.Text("Item 2")),
                    ft.MenuItemButton(content=ft.Text("Item 3")),
                ],
            ),
        ],
    )
    flet_app_function.page.add(mb)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    btn = await flet_app_function.tester.find_by_text("Submenu")
    await flet_app_function.tester.tap(btn)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": nested_submenus.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_nested_submenus(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "nested_submenus1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    smb = await flet_app_function.tester.find_by_text("File")
    await flet_app_function.tester.tap(smb)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "nested_submenus2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    mib = await flet_app_function.tester.find_by_text("Save")
    await flet_app_function.tester.tap(mib)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "nested_submenus3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["nested_submenus1", "nested_submenus2", "nested_submenus3"],
        "nested_submenus",
        duration=1600,
    )
