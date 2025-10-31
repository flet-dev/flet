import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Checkbox(),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp):
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
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)

    scr_1 = ft.Screenshot(cb := ft.Checkbox(key="cb", value=True, margin=20))
    flet_app.page.add(scr_1)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    # hover to check overlay color and splash radius
    checkbox = await flet_app.tester.find_by_key("cb")
    assert checkbox.count == 1
    await flet_app.tester.mouse_hover(checkbox)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_2",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    # uncheck the checkbox to test border side
    cb.value = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_3",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
