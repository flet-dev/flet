import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(500, 300)
    flet_app.page.show_dialog(ft.SnackBar(ft.Text("Hello, world!")))
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_simple_action(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(500, 300)
    flet_app.page.show_dialog(ft.SnackBar(ft.Text("Directory deleted."), action="Undo"))
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_custom_action(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(500, 300)
    flet_app.page.show_dialog(
        ft.SnackBar(
            ft.Text("File deleted."),
            action=ft.SnackBarAction(
                label="Undo delete",
                text_color=ft.Colors.YELLOW,
                bgcolor=ft.Colors.BLUE,
            ),
        )
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_page(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(500, 300)
    flet_app.page.platform = ft.PagePlatform.MACOS
    flet_app.page.adaptive = True
    flet_app.page.update()

    flet_app.page.show_dialog(ft.SnackBar("Snackbar in cupertino page."))
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
