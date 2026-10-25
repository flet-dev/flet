import pytest

import flet as ft
import flet.testing as ftt


def _refresh_content() -> ft.ListView:
    """A small scrollable child reused across tests."""
    return ft.ListView(
        controls=[
            ft.ListTile("List Tile 1"),
            ft.ListTile("List Tile 2"),
            ft.ListTile("List Tile 3"),
        ]
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_color(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            color=ft.Colors.RED,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_bgcolor(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_elevation(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            elevation=10.0,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_stroke_width(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            stroke_width=5.0,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_displacement_and_edge_offset(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            displacement=80.0,
            edge_offset=20.0,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_trigger_mode_anywhere(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            trigger_mode=ft.RefreshIndicatorTriggerMode.ANYWHERE,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_handle_nested_scrolls(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            handle_nested_scrolls=True,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_semantics(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            semantics_label="Refresh list",
            semantics_value="Loading new items",
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_handlers(flet_app: ftt.FletTestApp, request):
    """Renders the same with an `on_refresh` handler."""

    async def handle_refresh(e: ft.Event[ft.RefreshIndicator]):
        pass

    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RefreshIndicator(
            content=_refresh_content(),
            on_refresh=handle_refresh,
        ),
    )
