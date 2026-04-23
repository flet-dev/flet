import pytest

import examples.controls.material.text_field.basic.main as basic
import flet as ft
import flet.testing as ftt
from examples.controls.material.text_field.handling_change_events.main import (
    main as handling_change_events,
)
from examples.controls.material.text_field.label_hint_helper_counter.main import (
    main as label_hint_helper_counter,
)
from examples.controls.material.text_field.multiline.main import main as multiline
from examples.controls.material.text_field.password.main import main as password
from examples.controls.material.text_field.prefix_and_suffix.main import (
    main as prefix_and_suffix,
)
from examples.controls.material.text_field.selection_change.main import (
    main as selection_change,
)
from examples.controls.material.text_field.styled.main import main as styled
from examples.controls.material.text_field.underlined_and_borderless.main import (
    main as underlined_and_borderless,
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


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": password}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_password(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 180)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    textfield = await flet_app_function.tester.find_by_key("password_textfield")

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("password_initial", initial_frame)
    frames = [initial_frame]

    await flet_app_function.tester.tap(textfield)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.enter_text(textfield, "password")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    reveal = await flet_app_function.tester.find_by_icon(ft.Icons.VISIBILITY)
    await flet_app_function.tester.tap(reveal.first)
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("password_final", final_frame)
    frames.append(final_frame)

    flet_app_function.create_gif(frames=frames, output_name="password", duration=1000)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": multiline}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_multiline(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 420)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    standard = await flet_app_function.tester.find_by_key("multiline_standard")
    auto_height = await flet_app_function.tester.find_by_key("multiline_auto_height")

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("multiline_initial", initial_frame)
    frames = [initial_frame]

    await flet_app_function.tester.tap(standard)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )
    await flet_app_function.tester.enter_text(standard, "flet")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(auto_height)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    for value in [
        "line1",
        "line1\nline2",
        "line1\nline2\nline3",
        "line1\nline2\nline3\nline4",
        "line1\nline2\nline3\nline4\nline5",
    ]:
        await flet_app_function.tester.enter_text(auto_height, value)
        await flet_app_function.tester.pump_and_settle()
        frames.append(
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            )
        )

        if value != "line1\nline2\nline3\nline4\nline5":
            await flet_app_function.tester.enter_text(auto_height, f"{value}\n")
            await flet_app_function.tester.pump_and_settle()
            frames.append(
                await flet_app_function.page.take_screenshot(
                    pixel_ratio=flet_app_function.screenshots_pixel_ratio
                )
            )

    final_frame = frames[-1]
    flet_app_function.assert_screenshot("multiline_final", final_frame)
    flet_app_function.create_gif(frames=frames, output_name="multiline", duration=1000)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": underlined_and_borderless}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_underlined_and_borderless(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 360)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    underlined = await flet_app_function.tester.find_by_key("underlined_field")
    underlined_filled = await flet_app_function.tester.find_by_key(
        "underlined_filled_field"
    )
    borderless = await flet_app_function.tester.find_by_key("borderless_field")
    borderless_filled = await flet_app_function.tester.find_by_key(
        "borderless_filled_field"
    )

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "underlined_and_borderless_initial", initial_frame
    )
    frames = [initial_frame]

    await flet_app_function.tester.tap(underlined)
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.enter_text(underlined, "eat")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(underlined_filled)
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.enter_text(underlined_filled, "code")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(borderless)
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.enter_text(borderless, "eat again")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(borderless_filled)
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.enter_text(borderless_filled, "code again")
    await flet_app_function.tester.pump_and_settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("underlined_and_borderless_final", final_frame)
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames, output_name="underlined_and_borderless", duration=1000
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": prefix_and_suffix}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_prefix_and_suffix(flet_app_function: ftt.FletTestApp):
    async def _settle():
        await flet_app_function.tester.pump_and_settle(ft.Duration(milliseconds=500))

    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 520)
    flet_app_function.page.update()
    await _settle()

    prefix = await flet_app_function.tester.find_by_key("prefix_field")
    suffix = await flet_app_function.tester.find_by_key("suffix_field")
    prefix_suffix = await flet_app_function.tester.find_by_key("prefix_suffix_field")
    color = await flet_app_function.tester.find_by_key("color_field")
    submit = await flet_app_function.tester.find_by_key("submit_button")

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("prefix_and_suffix_initial", initial_frame)
    frames = [initial_frame]

    await flet_app_function.tester.tap(prefix)
    await _settle()
    await flet_app_function.tester.enter_text(prefix, "google.com")
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(suffix)
    await _settle()
    await flet_app_function.tester.enter_text(suffix, "github")
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(prefix_suffix)
    await _settle()
    await flet_app_function.tester.enter_text(prefix_suffix, "github")
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(color)
    await _settle()
    await flet_app_function.tester.enter_text(color, "red")
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.mouse_hover(submit)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(submit)
    await _settle()
    final_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("prefix_and_suffix_final", final_frame)
    frames.append(final_frame)

    flet_app_function.create_gif(
        frames=frames, output_name="prefix_and_suffix", duration=1000
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": styled}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_styled(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 260)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    textfield = await flet_app_function.tester.find_by_key("styled_textfield")
    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("styled_initial", initial_frame)
    frames = [initial_frame]

    await flet_app_function.tester.tap(textfield)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    for value in [
        "hello",
        "hello flet",
        "hello flet hello",
        "hello flet hello flet",
    ]:
        await flet_app_function.tester.enter_text(textfield, value)
        await flet_app_function.tester.pump_and_settle()
        frames.append(
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            )
        )

    final_frame = frames[-1]
    flet_app_function.assert_screenshot("styled_final", final_frame)
    flet_app_function.create_gif(frames=frames, output_name="styled", duration=1000)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": label_hint_helper_counter}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_label_hint_helper_counter(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 260)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    textfield = await flet_app_function.tester.find_by_key(
        "label_hint_helper_counter_textfield"
    )
    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "label_hint_helper_counter_initial", initial_frame
    )
    frames = [initial_frame]

    await flet_app_function.tester.tap(textfield)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    for value in [
        "first",
        "first name",
        "first name last",
        "first name last name",
    ]:
        await flet_app_function.tester.enter_text(textfield, value)
        await flet_app_function.tester.pump_and_settle()
        frames.append(
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            )
        )

    final_frame = frames[-1]
    flet_app_function.assert_screenshot("label_hint_helper_counter_final", final_frame)
    flet_app_function.create_gif(
        frames=frames, output_name="label_hint_helper_counter", duration=1000
    )
