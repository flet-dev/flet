import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    async def handle_tile_click(e: ft.Event[ft.ListTile]):
        await sb.close_view(e.control.title.value)

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        print("handle_tap")
        await sb.open_view()

    sb = ft.SearchBar(
        key="sb",
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f"Color {i}"), on_click=handle_tile_click)
            for i in range(10)
        ],
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [sb]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("sb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "basic_opened",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
