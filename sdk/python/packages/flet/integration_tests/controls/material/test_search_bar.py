import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    async def handle_tap(e: ft.Event[ft.SearchBar]):
        print("handle_tap")
        await sb.open_view()

    sb = ft.SearchBar(
        key="sb",
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_tap=handle_tap,
        controls=[ft.ListTile(title=ft.Text(f"Color {i}")) for i in range(10)],
    )

    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.add(sb)
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


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        search_bar_theme=ft.SearchBarTheme(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            text_capitalization=ft.TextCapitalization.SENTENCES,
            shadow_color=ft.Colors.YELLOW,
            overlay_color=ft.Colors.PURPLE,
            padding=ft.Padding(10, 20, 50, 20),
            elevation=100,
            text_style=ft.TextStyle(color=ft.Colors.RED, italic=True, size=30),
            hint_style=ft.TextStyle(color=ft.Colors.PINK, size=20, italic=True),
            shape=ft.RoundedRectangleBorder(
                radius=ft.BorderRadius.all(50),
            ),
            border_side=ft.BorderSide(color=ft.Colors.PURPLE, width=2),
        ),
        search_view_theme=ft.SearchViewTheme(
            bgcolor=ft.Colors.PURPLE_200,
            divider_color=ft.Colors.BLUE_800,
            elevation=30,
            header_hint_text_style=ft.TextStyle(
                color=ft.Colors.BLUE, size=20, italic=True
            ),
            header_text_style=ft.TextStyle(color=ft.Colors.GREEN, size=20, italic=True),
            shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius.all(20)),
            border_side=ft.BorderSide(color=ft.Colors.PURPLE, width=2),
            size_constraints=ft.BoxConstraints(
                min_width=400, max_width=400, min_height=400, max_height=400
            ),
            header_height=100,
            padding=ft.Padding(10, 20, 50, 20),
            bar_padding=ft.Padding.all(5),
            shrink_wrap=True,
        ),
    )

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        print("handle_tap")
        await sb.open_view()

    sb = ft.SearchBar(
        key="sb",
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_tap=handle_tap,
        controls=[ft.ListTile(title=ft.Text(f"Color {i}")) for i in range(10)],
    )

    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.add(sb)
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "theme",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # hover to check overlay color
    await flet_app.tester.mouse_hover(await flet_app.tester.find_by_key("sb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "theme_hovered",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("sb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "theme_opened",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
