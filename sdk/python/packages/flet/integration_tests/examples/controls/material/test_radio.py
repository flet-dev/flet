import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.radio.basic.main import main as basic
from examples.controls.material.radio.handling_selection_changes.main import (
    main as handling_selection_changes,
)
from examples.controls.material.radio.styled.main import main as styled


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
    # Hover over radio doesn't show on screenshot
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
    flet_app_function.resize_page(420, 250)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "handling_selection_changes_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]

    red = await flet_app_function.tester.find_by_text("Red")
    # Hover over radio doesn't show on screenshot
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

    green = await flet_app_function.tester.find_by_text("Green")
    await flet_app_function.tester.mouse_hover(green)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(green)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    blue = await flet_app_function.tester.find_by_text("Blue")
    await flet_app_function.tester.mouse_hover(blue)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(blue)
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "handling_selection_changes_final",
        final_frame,
    )
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames,
        output_name="handling_selection_changes",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": styled}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_styled(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.resize_page(500, 260)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "styled_initial",
        initial_frame,
    )
    frames: list[bytes] = [initial_frame]

    default_radio = await flet_app_function.tester.find_by_key("styled_radio_default")
    await flet_app_function.tester.mouse_hover(default_radio)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    default_label = await flet_app_function.tester.find_by_text(
        "Radio with default style"
    )
    await flet_app_function.tester.tap(default_label)
    await flet_app_function.tester.pump_and_settle()
    default_selected_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "styled_default_selected",
        default_selected_frame,
    )
    frames.append(default_selected_frame)

    constant_radio = await flet_app_function.tester.find_by_key("styled_radio_constant")
    await flet_app_function.tester.mouse_hover(constant_radio)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    constant_label = await flet_app_function.tester.find_by_text(
        "Radio with constant fill color"
    )
    await flet_app_function.tester.tap(constant_label)
    await flet_app_function.tester.pump_and_settle()
    constant_selected_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "styled_constant_selected",
        constant_selected_frame,
    )
    frames.append(constant_selected_frame)

    dynamic_radio = await flet_app_function.tester.find_by_key("styled_radio_dynamic")
    await flet_app_function.tester.mouse_hover(dynamic_radio)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    dynamic_label = await flet_app_function.tester.find_by_text(
        "Radio with dynamic fill color"
    )
    await flet_app_function.tester.tap(dynamic_label)
    await flet_app_function.tester.pump_and_settle()
    dynamic_selected_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "styled_dynamic_selected",
        dynamic_selected_frame,
    )
    frames.append(dynamic_selected_frame)

    flet_app_function.create_gif(
        frames=frames,
        output_name="styled",
        duration=1000,
    )
