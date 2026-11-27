import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.list_tile.main as list_tile
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=280,
            controls=[
                fluent.ListTile(
                    title="Inbox",
                    subtitle="3 unread messages",
                    leading=fluent.FluentIcons.MAIL,
                    selection_mode=fluent.ListTileSelectionMode.SINGLE,
                    selected=True,
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": list_tile.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_list_tile(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "list_tile_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await tester.tap(await tester.find_by_text("Sent"))
    await tester.pump_and_settle()

    assert (await tester.find_by_text("Folder: Sent")).count == 1
    flet_app_function.assert_screenshot(
        "list_tile",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["list_tile_initial", "list_tile"], "list_tile_flow", duration=1000
    )
