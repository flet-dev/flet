import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.auto_suggest_box.main as auto_suggest_box
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The suggestions open in an overlay, so these are full-page screenshots.
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=260,
            controls=[
                fluent.AutoSuggestBox(
                    placeholder="Search fruit",
                    items=[
                        fluent.AutoSuggestBoxItem(value="apple", label="Apple"),
                        fluent.AutoSuggestBoxItem(value="banana", label="Banana"),
                        fluent.AutoSuggestBoxItem(value="cherry", label="Cherry"),
                    ],
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": auto_suggest_box.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_auto_suggest_box(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(360, 300)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "auto_suggest_box_initial")

    # "L" matches Berlin, Lisbon and London.
    await tester.enter_text(await tester.find_by_key("city"), "L")
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Lisbon")).count == 1
    assert (await tester.find_by_text("Paris")).count == 0
    await _capture(flet_app_function, "auto_suggest_box_open")

    await tester.tap(await tester.find_by_text("London"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Destination: London")).count == 1
    await _capture(flet_app_function, "auto_suggest_box")
    flet_app_function.create_gif(
        ["auto_suggest_box_initial", "auto_suggest_box_open", "auto_suggest_box"],
        "auto_suggest_box_flow",
        duration=1000,
    )
