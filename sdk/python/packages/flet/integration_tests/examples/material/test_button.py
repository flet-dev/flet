import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.button import (
    animate_on_hover,
    basic,
    button_shapes,
    custom_content,
    handling_clicks,
    icons,
    styling,
)


@pytest.mark.asyncio(loop_scope="module")
async def test_image_for_docs(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                ft.Button(content="Enabled button"),
                ft.Button(content="Disabled button", disabled=True),
            ]
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": icons.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_icons(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "icons",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_content.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_content(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "custom_content",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_clicks.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_clicks(flet_app_function: ftt.FletTestApp):
    scr = await flet_app_function.wrap_page_controls_in_screenshot()
    button = await flet_app_function.tester.find_by_text("Button with 'click' event")
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_clicks",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": button_shapes.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_button_shapes(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "button_shapes",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": styling.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_styling(flet_app_function: ftt.FletTestApp):
    scr = await flet_app_function.wrap_page_controls_in_screenshot()
    flet_app_function.assert_screenshot(
        "styled_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    button = await flet_app_function.tester.find_by_text_containing("Styled")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "styled_hovered",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": animate_on_hover.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_animate_on_hover(flet_app_function: ftt.FletTestApp):
    scr = await flet_app_function.wrap_page_controls_in_screenshot(margin=20)
    flet_app_function.assert_screenshot(
        "animate_on_hover_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    button = await flet_app_function.tester.find_by_text_containing("Hover over me")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "animate_on_hover_hovered",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
        similarity_threshold=98.8,
    )
