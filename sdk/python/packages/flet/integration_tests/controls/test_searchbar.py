import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_searchbar(flet_app: ftt.FletTestApp, request):
    sb = ft.SearchBar(
        key="sb",
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        controls=[ft.ListTile(title=ft.Text(f"Color {i}")) for i in range(10)],
    )
    c = ft.Container(
        padding=ft.Padding.only(top=40),
        content=sb,
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [sb]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "empty",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    await sb.open_view()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "list",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
