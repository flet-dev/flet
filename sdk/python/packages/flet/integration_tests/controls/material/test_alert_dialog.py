import asyncio

import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_alert_dialog_basic(flet_app: ftt.FletTestApp, request):
    ad = ft.AlertDialog(
        key="ad",
        title=ft.Text("Hello"),
        content=ft.Text("You are notified!"),
        alignment=ft.Alignment.CENTER,
        on_dismiss=lambda e: print("Dialog dismissed!"),
        title_padding=ft.Padding.all(25),
    )
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.show_dialog(ad)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_update_body(flet_app: ftt.FletTestApp, request):
    ad = ft.AlertDialog(
        key="ad",
        title=ft.Text("Test"),
        bgcolor=ft.Colors.YELLOW,
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[
            ok := ft.TextButton(
                "OK",
                visible=True,
            ),
            cancel := ft.TextButton(
                "Cancel",
                visible=True,
            ),
        ],
    )
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.show_dialog(ad)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("OK")).count == 1

    flet_app.assert_screenshot(
        "update_body_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # change dialog color and hide "OK" button
    await asyncio.sleep(1)
    ad.bgcolor = ft.Colors.RED
    ok.visible = not ok.visible  # hide button
    cancel.disabled = not cancel.disabled  # disable button
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("OK")).count == 0

    flet_app.assert_screenshot(
        "update_body_2",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
