import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.popup_menu_button.basic.main import main as basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(100, 200)
    flet_app_function.page.update()
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.add(
        ft.PopupMenuButton(
            key="popup",
            items=[
                ft.PopupMenuItem(content="Sm"),
                ft.PopupMenuItem(content="Med"),
                ft.PopupMenuItem(content="Lg"),
            ],
            menu_position=ft.PopupMenuPosition.UNDER,
        )
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    pb = await flet_app_function.tester.find_by_key("popup")
    await flet_app_function.tester.tap(pb)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.page.update()
    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 240)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    pb = await flet_app_function.tester.find_by_key("popup")
    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio,
    )
    flet_app_function.assert_screenshot(
        "basic_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]

    await flet_app_function.tester.mouse_hover(pb)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
        )
    )

    await flet_app_function.tester.tap(pb)
    await flet_app_function.tester.pump_and_settle()
    open_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio,
    )
    flet_app_function.assert_screenshot(
        "basic_open",
        open_frame,
    )
    frames.append(open_frame)

    check_power = await flet_app_function.tester.find_by_text("Check power")
    await flet_app_function.tester.mouse_hover(check_power)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
        )
    )

    await flet_app_function.tester.tap(check_power)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
        )
    )

    flet_app_function.create_gif(
        frames=frames,
        output_name="basic",
        duration=1000,
    )
