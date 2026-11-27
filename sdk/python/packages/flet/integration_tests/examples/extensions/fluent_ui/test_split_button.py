import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.split_button.main as split_button
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
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Row(
            tight=True,
            controls=[
                fluent.SplitButton(
                    "Paste",
                    items=[
                        fluent.MenuFlyoutItem("Paste as text"),
                        fluent.MenuFlyoutItem("Paste with formatting"),
                    ],
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": split_button.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_split_button(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(360, 260)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "split_button_initial")

    await tester.tap(await tester.find_by_text("Highlight: Yellow"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "split_button_highlighted")

    # The chevron has no text or Flet icon to find it by.
    await tester.tap_at(ft.Offset(158, 26))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "split_button_open")

    await tester.tap(await tester.find_by_text("Green"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Highlight: Green")).count == 1
    await _capture(flet_app_function, "split_button")
    flet_app_function.create_gif(
        [
            "split_button_initial",
            "split_button_highlighted",
            "split_button_open",
            "split_button",
        ],
        "split_button_flow",
        duration=1000,
    )
