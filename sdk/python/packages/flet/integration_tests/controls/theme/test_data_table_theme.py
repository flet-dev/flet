import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_1(flet_app: ftt.FletTestApp, request):
    flet_app.resize_page(400, 600)
    flet_app.page.theme = ft.Theme(
        data_table_theme=ft.DataTableTheme(
            checkbox_horizontal_margin=10,
            column_spacing=50,
            data_row_max_height=200,
            data_row_min_height=0,
            data_row_color=ft.Colors.GREEN_200,
            data_text_style=ft.TextStyle(color=ft.Colors.GREEN_800),
            divider_thickness=10,
            horizontal_margin=20,
            heading_text_style=ft.TextStyle(italic=True),
            heading_row_color=ft.Colors.ORANGE_200,
            heading_row_height=100,
            data_row_cursor=ft.MouseCursor.FORBIDDEN,  # doesn't show on screenshot
            heading_row_alignment=ft.MainAxisAlignment.START,
            heading_cell_cursor=ft.MouseCursor.HELP,  # doesn't show on screenshot
            decoration=ft.BoxDecoration(
                shape=ft.BoxShape.RECTANGLE,
                bgcolor=ft.Colors.PURPLE_100,
                border=ft.Border.all(color=ft.Colors.RED),
            ),
        ),
        divider_theme=ft.DividerTheme(
            color=ft.Colors.GREEN,
            thickness=5,
        ),
    )

    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.DataTable(
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(label="Column 1"),
                ft.DataColumn(label=ft.Text("Column 2")),
                ft.DataColumn(label=ft.Text("Column 3")),
            ],
            rows=[
                ft.DataRow(
                    on_select_change=lambda e: print(f"Selected row {e.data}"),
                    cells=[
                        ft.DataCell("Item 1"),
                        ft.DataCell(ft.Text("Item 2")),
                        ft.DataCell(ft.Text("Item 3")),
                    ],
                ),
                ft.DataRow(
                    on_select_change=lambda e: print(f"Selected row {e.data}"),
                    cells=[
                        ft.DataCell("Item 1"),
                        ft.DataCell(ft.Text("Item 2")),
                        ft.DataCell(ft.Text("Item 3")),
                    ],
                ),
            ],
        ),
    )
