import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.menu_bar.nested_submenus import main as nested_submenus


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(150, 200)
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
    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "nested_submenus_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]
    smb = await flet_app_function.tester.find_by_text("File")
    await flet_app_function.tester.mouse_hover(smb)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )
    await flet_app_function.tester.tap(smb)
    await flet_app_function.tester.pump_and_settle()
    menu_open_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "nested_submenus_menu_open",
        menu_open_frame,
    )
    frames.append(menu_open_frame)
    mib = await flet_app_function.tester.find_by_text("Save")
    await flet_app_function.tester.mouse_hover(mib)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )
    await flet_app_function.tester.tap(mib)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    flet_app_function.create_gif(
        frames=frames,
        output_name="nested_submenus",
        duration=1600,
    )
