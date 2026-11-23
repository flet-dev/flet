import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.tooltip.main as tooltip
import flet as ft
import flet.testing as ftt


async def _hover_and_capture(app: ftt.FletTestApp, finder, name: str):
    # The tooltip opens in an overlay after a hover delay, so the clock is
    # advanced past the delay and a full-page screenshot is taken.
    await app.tester.mouse_hover(finder)
    await app.tester.pump(duration=ft.Duration(seconds=2))
    await app.tester.pump_and_settle()
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(260, 120)
    flet_app_function.page.add(
        ft.Container(
            padding=ft.Padding.only(left=40),
            content=fluent.Tooltip(
                message="Add to library",
                content=fluent.Button("Hover me"),
            ),
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _hover_and_capture(
        flet_app_function,
        await flet_app_function.tester.find_by_text("Hover me"),
        request.node.name,
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": tooltip.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 140)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Save the document")).count == 0
    await _hover_and_capture(
        flet_app_function,
        (await flet_app_function.tester.find_by_icon(fluent.FluentIcons.SAVE)),
        "tooltip",
    )
    assert (await flet_app_function.tester.find_by_text("Save the document")).count == 1
