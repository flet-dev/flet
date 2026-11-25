import sys

import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.tab_view.main as tab_view
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


# The close button's tooltip names the platform's shortcut.
CLOSE_TAB = "Close tab (Cmd+W)" if sys.platform == "darwin" else "Close tab (Ctrl+F4)"


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=400,
            controls=[
                fluent.TabView(
                    height=200,
                    tabs=[
                        fluent.Tab("Home", content=ft.Text("Welcome home")),
                        fluent.Tab("Settings", content=ft.Text("Your settings")),
                    ],
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": tab_view.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_tab_view(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 240)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "tab_view_initial")

    await tester.tap(await tester.find_by_tooltip("Add new tab"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Contents of document 3")).count == 1
    await _capture(flet_app_function, "tab_view_added")

    # Closing the first tab keeps the third one selected.
    await tester.tap((await tester.find_by_tooltip(CLOSE_TAB)).first)
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Document 1")).count == 0
    assert (await tester.find_by_text("Contents of document 3")).count == 1
    await _capture(flet_app_function, "tab_view_closed")

    await tester.tap(await tester.find_by_text("Document 2"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Contents of document 2")).count == 1
    await _capture(flet_app_function, "tab_view")
    flet_app_function.create_gif(
        ["tab_view_initial", "tab_view_added", "tab_view_closed", "tab_view"],
        "tab_view_flow",
        duration=1000,
    )
