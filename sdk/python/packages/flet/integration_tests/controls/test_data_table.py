import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
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


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp):
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
        )
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    scr_1 = ft.Screenshot(
        ft.DataTable(
            # bgcolor=ft.Colors.BLUE_100,
            show_checkbox_column=True,
            # border=ft.Border.all(color=ft.Colors.RED),
            # border_radius=30,
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
        )
    )
    flet_app.page.add(scr_1)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
