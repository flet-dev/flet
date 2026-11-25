import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.flyout.main as flyout
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The flyout opens over the page, so these are full-page screenshots.
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
    flet_app_function.resize_page(360, 200)

    def toggle(e):
        fl.open = not fl.open

    fl = fluent.Flyout(
        content=fluent.Button("Empty cart", on_click=toggle),
        flyout=ft.Text("All items will be removed. Do you want to continue?"),
    )
    page.add(ft.Row(controls=[fl], alignment=ft.MainAxisAlignment.CENTER))
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_text("Empty cart"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": flyout.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_flyout(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(360, 260)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "flyout_initial")

    await tester.tap(await tester.find_by_text("Empty cart"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "flyout_open")

    await tester.tap(await tester.find_by_text("Yes, empty my cart"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Your cart is empty")).count == 1
    assert (await tester.find_by_text("Yes, empty my cart")).count == 0
    await _capture(flet_app_function, "flyout")
    flet_app_function.create_gif(
        ["flyout_initial", "flyout_open", "flyout"],
        "flyout_flow",
        duration=1000,
    )
