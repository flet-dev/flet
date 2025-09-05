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
        ft.FloatingActionButton("OK"),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_location(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.floating_action_button = ft.FloatingActionButton("OK")

    # center_top_location
    loc = ft.FloatingActionButtonLocation.CENTER_TOP
    flet_app.page.floating_action_button_location = loc
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "center_top_location",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # end_top_location
    loc = ft.FloatingActionButtonLocation.END_TOP
    flet_app.page.floating_action_button_location = loc
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "end_top_location",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
