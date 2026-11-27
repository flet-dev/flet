import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.scaffold_page.main as scaffold_page
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    page.padding = 0
    flet_app_function.resize_page(400, 200)
    page.add(
        fluent.ScaffoldPage(
            expand=True,
            header=fluent.PageHeader(title="Inbox"),
            content=ft.Text("No new messages"),
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": scaffold_page.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_scaffold_page(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(720, 200)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "scaffold_page_initial")

    await tester.tap(await tester.find_by_text("Import"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("5 photos")).count == 1
    await _capture(flet_app_function, "scaffold_page")
    flet_app_function.create_gif(
        ["scaffold_page_initial", "scaffold_page"],
        "scaffold_page_flow",
        duration=1000,
    )
