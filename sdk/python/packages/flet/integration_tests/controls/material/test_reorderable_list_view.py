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
    flet_app.resize_page(400, 600)
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ReorderableListView(
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Draggable Item {i}"),
                )
                for i in range(5)
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_custom_drag_handle(flet_app: ftt.FletTestApp, request):
    flet_app.resize_page(400, 600)
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ReorderableListView(
            show_default_drag_handles=False,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                    leading=ft.ReorderableDragHandle(
                        content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
                        mouse_cursor=ft.MouseCursor.GRAB,
                    ),
                    bgcolor=ft.Colors.ERROR
                    if i % 2 == 0
                    else ft.Colors.ON_ERROR_CONTAINER,
                )
                for i in range(5)
            ],
        ),
    )
