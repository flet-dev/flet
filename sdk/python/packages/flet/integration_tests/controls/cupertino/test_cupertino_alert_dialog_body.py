import asyncio

import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_update_body(flet_app: ftt.FletTestApp, request):
    ad = ft.CupertinoAlertDialog(
        key="ad",
        title=ft.Text("Test"),
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
    await flet_app.resize_page(400, 600)
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
