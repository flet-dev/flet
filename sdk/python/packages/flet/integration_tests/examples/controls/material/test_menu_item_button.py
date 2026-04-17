import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.menu_item_button.basic import main as basic


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
    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "basic_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]
    btn = await flet_app_function.tester.find_by_text("BgColors")
    await flet_app_function.tester.mouse_hover(btn)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )
    await flet_app_function.tester.tap(btn)
    await flet_app_function.tester.pump_and_settle()
    open_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "basic_open",
        open_frame,
    )
    frames.append(open_frame)
    mib = await flet_app_function.tester.find_by_text("Green")
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
        output_name="basic",
        duration=1600,
    )
