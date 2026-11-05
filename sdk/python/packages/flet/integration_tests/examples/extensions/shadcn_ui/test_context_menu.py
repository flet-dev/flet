import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.context_menu.main as context_menu
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    # The menu opens in an overlay, so this is a full-page screenshot.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(360, 260)
    flet_app_function.page.add(
        shad.ContextMenu(
            content=ft.Container(
                key="area",
                width=200,
                height=80,
                alignment=ft.Alignment.CENTER,
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
                content=ft.Text("Right click here"),
            ),
            items=[
                shad.MenuItem("Back", trailing="Ctrl+["),
                shad.MenuItem("Reload", trailing="Ctrl+R"),
                shad.Separator(margin=ft.Margin.symmetric(vertical=4)),
                shad.MenuItem("Bookmarks", leading=shad.LucideIcons.BOOKMARK),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.right_mouse_click(
        await flet_app_function.tester.find_by_key("area")
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": context_menu.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_context_menu(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(560, 420)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.right_mouse_click(
        await flet_app_function.tester.find_by_key("area")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Reload")).count == 1
    await _capture(flet_app_function, "context_menu_open")

    await flet_app_function.tester.mouse_hover(
        await flet_app_function.tester.find_by_text("More Tools")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Developer Tools")).count == 1
    await _capture(flet_app_function, "context_menu_submenu")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Developer Tools")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (
        await flet_app_function.tester.find_by_text("Clicked: Developer Tools")
    ).count == 1
    assert (await flet_app_function.tester.find_by_text("Reload")).count == 0
    await _capture(flet_app_function, "context_menu")
    flet_app_function.create_gif(
        ["context_menu_open", "context_menu_submenu", "context_menu"],
        "context_menu_flow",
        duration=1000,
    )
