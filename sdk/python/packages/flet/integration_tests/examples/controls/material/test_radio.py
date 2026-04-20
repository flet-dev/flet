import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.radio.basic.main import main as basic
from examples.controls.material.radio.handling_selection_changes.main import (
    main as handling_selection_changes,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.RadioGroup(
            content=ft.Row(
                controls=[ft.Radio(label=f"{i}") for i in range(1, 4)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
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
    flet_app_function.resize_page(420, 280)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "basic_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]

    red = await flet_app_function.tester.find_by_text("Red")
    await flet_app_function.tester.mouse_hover(red)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(red)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    submit = await flet_app_function.tester.find_by_key("basic_submit_button")
    await flet_app_function.tester.mouse_hover(submit)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(submit)
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "basic_final",
        final_frame,
    )
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames,
        output_name="basic",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_selection_changes}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_selection_changes(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    blue = await flet_app_function.tester.find_by_text("Blue")
    await flet_app_function.tester.tap(blue)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_selection_changes",
        await flet_app_function.take_page_controls_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
