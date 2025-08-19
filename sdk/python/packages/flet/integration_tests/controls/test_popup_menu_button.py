import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    pb = ft.PopupMenuButton(
        key="pb",
        items=[
            ft.PopupMenuItem("Item 1"),
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, content="Check power"),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                        ft.Text("Item with a custom content"),
                    ]
                ),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                content="Checked item",
                checked=False,
            ),
        ],
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [pb]
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
    await flet_app.tester.tap(await flet_app.tester.find_by_key("pb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "basic_opened",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp, request):
    pb = ft.PopupMenuButton(
        size_constraints=ft.BoxConstraints(min_width=200, max_width=300),
        key="pb",
        items=[
            ft.PopupMenuItem("Item 1"),
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, content="Check power"),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                        ft.Text("Item with a custom content"),
                    ]
                ),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                content="Checked item",
                checked=False,
            ),
        ],
    )
    flet_app.page.theme = ft.Theme(
        popup_menu_theme=ft.PopupMenuTheme(
            # color=ft.Colors.RED,
            surface_tint_color=ft.Colors.GREEN,
            elevation=20,
            shadow_color=ft.Colors.BLUE,
            icon_color=ft.Colors.ORANGE_600,
            enable_feedback=True,
            icon_size=30,
            shape=ft.RoundedRectangleBorder(
                radius=ft.BorderRadius.all(10),
                side=ft.BorderSide(color=ft.Colors.GREEN_900, width=2),
            ),
            label_text_style=ft.TextStyle(size=15, color=ft.Colors.GREEN_500),
            menu_position=ft.PopupMenuPosition.OVER,
            mouse_cursor=ft.MouseCursor.GRAB,
            menu_padding=ft.Padding.all(20),
        ),
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [pb]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "theme",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("pb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "theme_opened",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
