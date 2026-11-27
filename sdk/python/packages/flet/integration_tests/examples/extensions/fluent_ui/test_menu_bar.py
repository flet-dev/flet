import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.menu_bar.main as menu_bar
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # Menus open over the page, so these are full-page screenshots.
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
    flet_app_function.resize_page(300, 200)
    page.add(
        fluent.MenuBar(
            items=[
                fluent.MenuBarItem(
                    "File",
                    items=[
                        fluent.MenuFlyoutItem("New", trailing="Ctrl+N"),
                        fluent.MenuFlyoutItem("Open...", trailing="Ctrl+O"),
                    ],
                ),
                fluent.MenuBarItem("Edit", items=[fluent.MenuFlyoutItem("Undo")]),
            ]
        )
    )
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_text("File"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": menu_bar.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_menu_bar(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(360, 300)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "menu_bar_initial")

    await tester.tap(await tester.find_by_text("Edit"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "menu_bar_open")

    await tester.tap(await tester.find_by_text("Copy"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Copy clicked")).count == 1
    await _capture(flet_app_function, "menu_bar_clicked")

    # Choosing large text enlarges the status text.
    await tester.tap(await tester.find_by_text("View"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "menu_bar_view")
    await tester.tap(await tester.find_by_text("Large text"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "menu_bar_large")

    # The radio items show the choice; turning off the status bar hides the
    # status text.
    await tester.tap(await tester.find_by_text("View"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "menu_bar_view_large")
    await tester.tap(await tester.find_by_text("Status bar"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Copy clicked")).count == 0
    await _capture(flet_app_function, "menu_bar")
    flet_app_function.create_gif(
        [
            "menu_bar_initial",
            "menu_bar_open",
            "menu_bar_clicked",
            "menu_bar_view",
            "menu_bar_large",
            "menu_bar_view_large",
            "menu_bar",
        ],
        "menu_bar_flow",
        duration=1000,
    )
