import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_navigation_rail(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.NavigationRail(
            height=400,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            on_change=lambda e: print(
                "Selected destination:", e.control.selected_index
            ),
            leading=ft.FloatingActionButton(
                icon=ft.Icons.CREATE,
                content="Add",
                on_click=lambda e: print("FAB clicked!"),
            ),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.FAVORITE_BORDER,
                    selected_icon=ft.Icons.FAVORITE,
                    label="First",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                    selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                    label="Second",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.SETTINGS),
                    label=ft.Text("Settings"),
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_navigation_rail_no_selected_icon(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.NavigationRail(
            height=400,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, content="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PHONE, badge="10"),
                    label="Calls",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.MAIL, badge=ft.Badge()),
                    label="Mail",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    # selected_icon=ft.Icon(ft.Icons.SETTINGS),
                    label=ft.Text("Settings"),
                ),
            ],
            on_change=lambda e: print(
                "Selected destination:", e.control.selected_index
            ),
        ),
    )
