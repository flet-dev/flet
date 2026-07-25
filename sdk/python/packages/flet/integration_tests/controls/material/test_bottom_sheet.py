import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)

    sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                controls=[
                    ft.Text("Here is a bottom sheet!"),
                    ft.Button("Dismiss", on_click=lambda _: flet_app.page.pop_dialog()),
                ],
            ),
        ),
    )
    flet_app.page.show_dialog(sheet)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_close_with_snackbar(flet_app: ftt.FletTestApp):
    # Exercises the fixed flow: dismissing the sheet and showing a SnackBar
    # from the SAME handler. This used to pop the sheet's route synchronously
    # during build (crashing with "setState() called during build" on-device);
    # the close is now deferred to a post-frame callback. The exact crash is a
    # device frame-timing race that `flutter test` doesn't reproduce, so this
    # guards the close+SnackBar flow rather than the raw crash.
    flet_app.resize_page(400, 600)

    def close_and_snack(_):
        flet_app.page.pop_dialog()
        flet_app.page.show_dialog(ft.SnackBar(content=ft.Text("Item deleted")))

    sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Actions"),
                    ft.Button("Delete", on_click=close_and_snack),
                ],
            ),
        ),
    )
    flet_app.page.show_dialog(sheet)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    delete_button = await flet_app.tester.find_by_text("Delete")
    assert delete_button.count == 1
    await flet_app.tester.tap(delete_button)
    # A crash here (or a failure to render the SnackBar) means the regression
    # is back.
    await flet_app.tester.pump_and_settle()

    snack = await flet_app.tester.find_by_text("Item deleted")
    assert snack.count == 1

    # Clean up so the module-scoped page doesn't leak the SnackBar.
    flet_app.page.pop_dialog()
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()


@pytest.mark.asyncio(loop_scope="module")
async def test_fullscreen(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)

    sheet = ft.BottomSheet(
        fullscreen=True,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                controls=[
                    ft.Text("Here is a bottom sheet!"),
                    ft.Button("Dismiss", on_click=lambda _: flet_app.page.pop_dialog()),
                ],
            ),
        ),
    )
    flet_app.page.show_dialog(sheet)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
