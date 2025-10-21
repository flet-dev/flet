import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.submenu_button import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    smb = ft.SubmenuButton(
        content=ft.Text("Choose text style"),
        key="smbutton",
        expand=True,
        menu_style=ft.MenuStyle(
            alignment=ft.Alignment.BOTTOM_LEFT, side=ft.BorderSide(1)
        ),
        controls=[
            ft.MenuItemButton(
                content=ft.Text("Underlined"),
                on_click=lambda e: print(f"{e.control.content.value}.on_click"),
                style=ft.ButtonStyle(
                    text_style={
                        ft.ControlState.HOVERED: ft.TextStyle(
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    }
                ),
            ),
            ft.MenuItemButton(
                content=ft.Text("Bold"),
                on_click=lambda e: print(f"{e.control.content.value}.on_click"),
                style=ft.ButtonStyle(
                    text_style={
                        ft.ControlState.HOVERED: ft.TextStyle(weight=ft.FontWeight.BOLD)
                    }
                ),
            ),
            ft.MenuItemButton(
                content=ft.Text("Italic"),
                on_click=lambda e: print(f"{e.control.content.value}.on_click"),
                style=ft.ButtonStyle(
                    text_style={ft.ControlState.HOVERED: ft.TextStyle(italic=True)}
                ),
            ),
        ],
    )
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.add(ft.Row(controls=[smb]))
    # flet_app_function.page.update()
    # await flet_app_function.tester.pump_and_settle()
    flet_app_function.page.window.width = 200
    flet_app_function.page.window.height = 200
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    button = await flet_app_function.tester.find_by_key("smbutton")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
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
    flet_app_function.page.window.width = 450
    flet_app_function.page.window.height = 400
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    button = await flet_app_function.tester.find_by_key("submenubutton")
    await flet_app_function.tester.tap(button)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
