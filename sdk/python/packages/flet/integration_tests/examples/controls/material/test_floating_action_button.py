import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.floating_action_button.handling_clicks import (
    main as handling_clicks,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.FloatingActionButton(icon=ft.Icons.ADD),
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
    flet_app_function.resize_page(420, 520)
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

    fab = await flet_app_function.tester.find_by_key("handling_clicks_fab")
    await flet_app_function.tester.mouse_hover(fab)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(fab)
    await flet_app_function.tester.pump_and_settle()
    last_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "handling_clicks_final",
        last_frame,
    )
    frames.append(last_frame)

    await flet_app_function.tester.mouse_hover(fab)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(fab)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.mouse_hover(fab)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(fab)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    flet_app_function.create_gif(
        frames=frames,
        output_name="handling_clicks",
        duration=1000,
    )
