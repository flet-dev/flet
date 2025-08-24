import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_banner_presence(flet_app: ftt.FletTestApp, request):
    action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)

    def handle_banner_close(e: ft.Event[ft.TextButton]):
        flet_app.page.pop_dialog()
        flet_app.page.add(ft.Text(f"Action clicked: {e.control.content}"))

    eb = ft.Button(
        "Show Banner", on_click=lambda e: flet_app.page.show_dialog(banner), key="eb"
    )
    banner = ft.Banner(
        key="banner",
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
        content=ft.Text(
            value="Oops, there were some errors while trying to delete the file. What "
            "would you like to do?",
            color=ft.Colors.BLACK,
        ),
        actions=[
            ft.TextButton(
                content="Retry",
                style=action_button_style,
                on_click=handle_banner_close,
                key="retry",
            ),
            ft.TextButton(
                content="Cancel",
                style=action_button_style,
                on_click=handle_banner_close,
                key="cancel",
            ),
        ],
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [eb]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap(await flet_app.tester.find_by_key("eb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "banner_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    await flet_app.tester.tap(await flet_app.tester.find_by_key("retry"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "banner_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_banner_string_content(flet_app: ftt.FletTestApp, request):
    banner = ft.Banner(
        "This is a banner with string content.",
        actions=[
            ft.TextButton("Retry"),
            ft.TextButton("Cancel"),
        ],
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(banner)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "banner_string_content",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
