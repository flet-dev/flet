import pytest

import examples.controls.alert_dialog.modal_and_non_modal.main as modal_and_non_modal
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 300)
    flet_app_function.page.update()

    flet_app_function.page.show_dialog(
        ft.AlertDialog(
            title=ft.Text("Session expired"),
            content=ft.Text("Please sign in again to continue."),
            actions=[ft.TextButton("Dismiss")],
            open=True,
        )
    )
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": modal_and_non_modal.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    button = await flet_app_function.tester.find_by_text_containing("Open dialog")
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "non_modal_dialog",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.page.pop_dialog()
    await flet_app_function.tester.pump_and_settle()
    modal_button = await flet_app_function.tester.find_by_text_containing(
        "Open modal dialog"
    )
    await flet_app_function.tester.tap(modal_button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "modal_dialog",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["before_click", "non_modal_dialog", "before_click", "modal_dialog"],
        "alert_dialog_flow",
        duration=2000,
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_use_dialog_dismiss_fires_after_animation(
    flet_app_function: ftt.FletTestApp,
):
    @ft.component
    def App():
        show, set_show = ft.use_state(False)
        status, set_status = ft.use_state("waiting")

        ft.use_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Delete report.pdf?"),
                content=ft.Text("This cannot be undone."),
                actions=[
                    ft.TextButton("Close", on_click=lambda: set_show(False)),
                ],
                on_dismiss=lambda: set_status("dismissed"),
            )
            if show
            else None
        )

        return ft.Column(
            controls=[
                ft.Text(status),
                ft.TextButton("Open", on_click=lambda: set_show(True)),
            ]
        )

    flet_app_function.page.render(App)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Open")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("waiting")).count == 1
    assert (
        await flet_app_function.tester.find_by_text("Delete report.pdf?")
    ).count == 1

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Close")
    )
    await flet_app_function.tester.pump()

    assert (await flet_app_function.tester.find_by_text("dismissed")).count == 0
    assert (await flet_app_function.tester.find_by_text("waiting")).count == 1

    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("dismissed")).count == 1
    assert (
        await flet_app_function.tester.find_by_text("Delete report.pdf?")
    ).count == 0
