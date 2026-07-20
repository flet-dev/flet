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
    flet_app.resize_page(400, 600)
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
    flet_app.resize_page(400, 600)
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


@pytest.mark.asyncio(loop_scope="function")
async def test_on_tap_outside_view(flet_app: ftt.FletTestApp):
    """
    `on_tap_outside_view` fires when the user taps outside the *open* search
    view (e.g. the dismiss barrier), but not when tapping the view's own field
    or a suggestion.
    Regression test for https://github.com/flet-dev/flet/issues/6593.
    """
    events = []

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        await sb.open_view()

    flet_app.page.padding = 0
    flet_app.resize_page(400, 700)
    flet_app.page.add(
        sb := ft.SearchBar(
            key="sb",
            bar_hint_text="Search...",
            on_tap=handle_tap,
            on_tap_outside_view=lambda e: events.append("outside_view"),
            # Keep the open view small so the surrounding barrier is easy to hit.
            view_size_constraints=ft.BoxConstraints(
                min_width=350, max_width=350, min_height=250, max_height=250
            ),
            controls=[ft.ListTile(title=ft.Text(f"Suggestion {i}")) for i in range(3)],
        )
    )
    await flet_app.tester.pump_and_settle()

    # Open the search view.
    await flet_app.tester.tap(await flet_app.tester.find_by_key("sb"))
    await flet_app.tester.pump_and_settle()
    assert events == []

    # Tapping a suggestion (inside the open view) must NOT fire the event.
    await flet_app.tester.tap(
        (await flet_app.tester.find_by_text("Suggestion 0")).first
    )
    await flet_app.tester.pump_and_settle()
    assert events == []

    # Tapping the view's own search field (its header, near the top of the
    # open view) must NOT fire the event either.
    await flet_app.tester.tap_at(ft.Offset(175, 28))
    await flet_app.tester.pump_and_settle()
    assert events == []

    # Tapping the barrier (outside the open view, well below the 250px-tall
    # view) fires the event and dismisses the view.
    await flet_app.tester.tap_at(ft.Offset(200, 660))
    await flet_app.tester.pump_and_settle()
    assert events == ["outside_view"]


@pytest.mark.asyncio(loop_scope="function")
async def test_on_tap_outside_bar(flet_app: ftt.FletTestApp):
    """
    `on_tap_outside_bar` fires when the bar is focused and the search view is
    closed, and the user taps away from the bar.
    """
    outside_bar_events = []
    focus_events = []

    # Note: no `on_tap` opening the view -> tapping the bar just focuses it.
    flet_app.page.padding = 0
    flet_app.resize_page(400, 600)
    flet_app.page.add(
        ft.SearchBar(
            key="sb",
            bar_hint_text="Search...",
            on_focus=lambda e: focus_events.append("focus"),
            on_tap_outside_bar=lambda e: outside_bar_events.append("outside_bar"),
        ),
        ft.Container(key="outside", width=200, height=200),
    )
    await flet_app.tester.pump_and_settle()

    # Tap the bar: it gains focus, the view stays closed.
    await flet_app.tester.tap(await flet_app.tester.find_by_key("sb"))
    await flet_app.tester.pump_and_settle()
    assert focus_events == ["focus"]
    assert outside_bar_events == []

    # Tap away from the focused, closed bar -> the event fires.
    await flet_app.tester.tap(await flet_app.tester.find_by_key("outside"))
    await flet_app.tester.pump_and_settle()
    assert outside_bar_events == ["outside_bar"]
