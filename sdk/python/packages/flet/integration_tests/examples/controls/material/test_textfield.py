import pytest

import examples.controls.material.text_field.basic.main as basic
import flet as ft
import flet.testing as ftt
from examples.controls.material.text_field.handling_change_events.main import (
    main as handling_change_events,
)
from examples.controls.material.text_field.selection_change.main import (
    main as selection_change,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.TextField(label="Name", hint_text="Jane Doe"),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.resize_page(500, 520)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_change_events}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_change_events(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(500, 220)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    textfield = await flet_app_function.tester.find_by_key("handling_change_textfield")

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("handling_change_events_initial", initial_frame)
    frames = [initial_frame]

    await flet_app_function.tester.tap(textfield)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.enter_text(textfield, "hello")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.enter_text(textfield, "hello flet")
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("handling_change_events_final", final_frame)
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames, output_name="handling_change_events", duration=1000
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": selection_change}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_selection_change(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 320)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("selection_change_initial", initial_frame)
    frames = [initial_frame]

    select_all = await flet_app_function.tester.find_by_text("Select all text")
    await flet_app_function.tester.mouse_hover(select_all)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(select_all)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    move_caret = await flet_app_function.tester.find_by_text("Move caret to start")
    await flet_app_function.tester.mouse_hover(move_caret)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(move_caret)
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("selection_change_final", final_frame)
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames, output_name="selection_change", duration=1000
    )
