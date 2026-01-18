import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.reorderable_list_view import horizontal_and_vertical


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ReorderableListView(
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Item {i}"),
                    bgcolor=ft.Colors.BLUE_GREY_300,
                )
                for i in range(1, 6)
            ],
            show_default_drag_handles=True,
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": horizontal_and_vertical.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_horizontal_and_vertical(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "horizontal_and_vertical",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
