import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.data_table import basic, sortable_and_selectable


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Name")),
                ft.DataColumn(label=ft.Text("Role")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Engineer")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Bob")),
                        ft.DataCell(ft.Text("Designer")),
                    ]
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(355, 260)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": sortable_and_selectable.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_sortable_and_selectable(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(500, 620)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "sortable_and_selectable",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
