import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.navigation_view.main as navigation_view
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
    flet_app_function.resize_page(700, 300)
    page.add(
        fluent.NavigationView(
            expand=True,
            selected_index=0,
            items=[
                fluent.PaneItem(
                    "Home",
                    icon=fluent.FluentIcons.HOME,
                    content=fluent.ScaffoldPage(content=ft.Text("Welcome home")),
                ),
                fluent.PaneItem(
                    "Mail",
                    icon=fluent.FluentIcons.MAIL,
                    content=fluent.ScaffoldPage(content=ft.Text("No new mail")),
                ),
            ],
            footer_items=[
                fluent.PaneItem(
                    "Settings",
                    icon=fluent.FluentIcons.SETTINGS,
                    content=fluent.ScaffoldPage(content=ft.Text("Settings")),
                ),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": navigation_view.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_navigation_view(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(720, 360)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    assert (await tester.find_by_text("You have 3 unread messages.")).count == 1
    await _capture(flet_app_function, "navigation_view_initial")

    # The window is too narrow for the expanded pane: the compact pane
    # opens over the content.
    await tester.tap(await tester.find_by_tooltip("Open Navigation"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "navigation_view_open")
    await tester.tap(await tester.find_by_text("Archive"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Archived messages.")).count == 1
    await _capture(flet_app_function, "navigation_view_archive")

    await tester.tap(await tester.find_by_icon(fluent.FluentIcons.SETTINGS))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Mail settings.")).count == 1
    await _capture(flet_app_function, "navigation_view")
    flet_app_function.create_gif(
        [
            "navigation_view_initial",
            "navigation_view_open",
            "navigation_view_archive",
            "navigation_view",
        ],
        "navigation_view_flow",
        duration=1000,
    )
