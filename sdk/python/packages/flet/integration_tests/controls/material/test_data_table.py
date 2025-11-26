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
