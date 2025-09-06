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
async def test_properties1(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FloatingActionButton(
            content="Add",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.GREEN,
            shape=ft.RoundedRectangleBorder(
                radius=4, side=ft.BorderSide(color=ft.Colors.RED, width=2.0)
            ),
            autofocus=False,
            foreground_color=ft.Colors.PURPLE,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # not shows on screenshot
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_properties2(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    fab = ft.FloatingActionButton(
        key="fab",
        content="Add",
        bgcolor=ft.Colors.GREEN,
        focus_color=ft.Colors.YELLOW,
        elevation=20,
        focus_elevation=50,
        disabled_elevation=30,
    )
    flet_app.page.add(fab)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "elevation",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test focus color
    fab.autofocus = True
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "focus",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test disabled
    fab.autofocus = False
    fab.disabled = True
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "disabled",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
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
