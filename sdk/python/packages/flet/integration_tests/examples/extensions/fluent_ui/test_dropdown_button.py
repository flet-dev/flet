import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.dropdown_button.main as dropdown_button
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The menu opens over the page, so these are full-page screenshots.
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    tester = flet_app_function.tester
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    flet_app_function.resize_page(260, 200)
    page.add(
        fluent.DropDownButton(
            "Sort by",
            items=[
                fluent.MenuFlyoutItem("Name"),
                fluent.MenuFlyoutItem("Date modified"),
                fluent.MenuFlyoutItem("Size"),
            ],
        )
    )
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_text("Sort by"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": dropdown_button.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_dropdown_button(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(360, 240)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "dropdown_button_initial")

    await tester.tap(await tester.find_by_key("sort"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "dropdown_button_open")

    await tester.tap(await tester.find_by_text("Size"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Sort by: Size")).count == 1
    await _capture(flet_app_function, "dropdown_button")
    flet_app_function.create_gif(
        ["dropdown_button_initial", "dropdown_button_open", "dropdown_button"],
        "dropdown_button_flow",
        duration=1000,
    )
