import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_data_table_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.DataTable(
            columns=[
                ft.DataColumn(label="Column 1"),
                ft.DataColumn(label=ft.Text("Column 2")),
                ft.DataColumn(label=ft.Text("Column 3")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell("Item 1"),
                        ft.DataCell(ft.Text("Item 2")),
                        ft.DataCell(ft.Text("Item 3")),
                    ]
                ),
            ],
        ),
    )
