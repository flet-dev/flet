import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.context_menu.main as context_menu
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
    flet_app_function.resize_page(360, 240)
    page.add(
        fluent.ContextMenu(
            key="area",
            content=ft.Container(width=300, height=150, content=ft.Text("Right click")),
            items=[
                fluent.MenuFlyoutItem("Back"),
                fluent.MenuFlyoutItem("Reload", trailing="Ctrl+R"),
            ],
        )
    )
    await tester.pump_and_settle()
    await tester.right_mouse_click(await tester.find_by_text("Right click"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": context_menu.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_context_menu(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 320)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "context_menu_initial")

    await tester.right_mouse_click(await tester.find_by_text("Report.docx"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "context_menu_open")

    # Clicking "Share" opens its submenu.
    await tester.tap(await tester.find_by_text("Share"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "context_menu_submenu")

    await tester.tap(await tester.find_by_text("Copy link"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Copy link: Report.docx")).count == 1
    await _capture(flet_app_function, "context_menu")
    flet_app_function.create_gif(
        [
            "context_menu_initial",
            "context_menu_open",
            "context_menu_submenu",
            "context_menu",
        ],
        "context_menu_flow",
        duration=1000,
    )
