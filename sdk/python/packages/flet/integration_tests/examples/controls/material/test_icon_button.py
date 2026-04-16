import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.icon_button.handling_clicks import (
    main as handling_clicks,
)
from examples.controls.material.icon_button.selected_icon import (
    main as selected_icon,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.PRIMARY),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_clicks.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_clicks(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 220)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "handling_clicks_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]

    button = await flet_app_function.tester.find_by_key("handling_clicks_icon_button")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "handling_clicks_final",
        final_frame,
    )
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames,
        output_name="handling_clicks",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": selected_icon.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_selected_icon(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 240)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "selected_icon_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]

    button = await flet_app_function.tester.find_by_key("selected_icon_button")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "selected_icon_final",
        final_frame,
    )
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames,
        output_name="selected_icon",
        duration=1000,
    )
