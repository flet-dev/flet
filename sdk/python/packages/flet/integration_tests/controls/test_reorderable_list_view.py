import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_reorderable_list_view_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ReorderableListView(
            # expand=True,
            controls=[
                ft.ReorderableDraggable(
                    index=i,
                    content=ft.Text(f"Item {i}"),
                )
                for i in range(5)
            ],
        ),
    )
