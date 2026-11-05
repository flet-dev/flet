import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.menubar.main as menubar
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
    flet_app_function.resize_page(360, 240)
    flet_app_function.page.add(
        shad.Menubar(
            items=[
                shad.MenubarItem(
                    "File",
                    items=[
                        shad.MenuItem("New Tab", trailing="Ctrl+T"),
                        shad.MenuItem("New Window", trailing="Ctrl+N"),
                        shad.Separator(margin=ft.Margin.symmetric(vertical=4)),
                        shad.MenuItem("Print...", trailing="Ctrl+P"),
                    ],
                ),
                shad.MenubarItem("Edit", items=[shad.MenuItem("Undo")]),
                shad.MenubarItem("View", items=[shad.MenuItem("Reload")]),
            ]
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("File")
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": menubar.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_menubar(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(560, 420)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("File")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("New Tab")).count == 1
    await _capture(flet_app_function, "menubar_open")

    await flet_app_function.tester.mouse_hover(
        await flet_app_function.tester.find_by_text("Share")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Messages")).count == 1
    await _capture(flet_app_function, "menubar_submenu")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Messages")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Clicked: Messages")).count == 1
    assert (await flet_app_function.tester.find_by_text("New Tab")).count == 0
    await _capture(flet_app_function, "menubar")
    flet_app_function.create_gif(
        ["menubar_open", "menubar_submenu", "menubar"], "menubar_flow", duration=1000
    )
