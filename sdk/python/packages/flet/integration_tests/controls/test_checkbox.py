import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_checkbox_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.add(ft.Checkbox())
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "checkbox_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_checkbox_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        checkbox_theme=ft.CheckboxTheme(
            check_color=ft.Colors.RED,
            overlay_color=ft.Colors.GREEN,
            fill_color=ft.Colors.BLUE,
            splash_radius=30,
            border_side=ft.BorderSide(color=ft.Colors.YELLOW, width=1),
            visual_density=ft.VisualDensity.COMPACT,
            shape=ft.BeveledRectangleBorder(radius=ft.BorderRadius.all(10)),
            mouse_cursor=ft.MouseCursor.FORBIDDEN,
        )
    )

    cb = ft.Checkbox(key="cb", value=True)
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.add(ft.Container(key="c", content=cb, padding=20))
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "checkbox_theme_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # hover to check overlay color and splash radius
    checkbox = await flet_app.tester.find_by_key("cb")
    assert checkbox.count == 1
    await flet_app.tester.mouse_hover(checkbox)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "checkbox_theme_2",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # uncheck the checkbox to test border side
    cb.value = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "checkbox_theme_3",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
