import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.teaching_tip.main as teaching_tip
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The tip opens over the page, so these are full-page screenshots.
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    tester = flet_app_function.tester
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    flet_app_function.resize_page(400, 260)
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                fluent.TeachingTip(
                    content=fluent.Button("Save"),
                    title="Save automatically",
                    subtitle="Changes are saved as you type, so you can close "
                    "this page at any time.",
                    open=True,
                )
            ],
        )
    )
    await tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": teaching_tip.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_teaching_tip(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 280)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "teaching_tip_initial")

    await tester.tap(await tester.find_by_text("What's new?"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Save your work")).count == 1
    await _capture(flet_app_function, "teaching_tip_open")

    await tester.tap(await tester.find_by_text("Got it"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Save your work")).count == 0
    await _capture(flet_app_function, "teaching_tip")
    flet_app_function.create_gif(
        ["teaching_tip_initial", "teaching_tip_open", "teaching_tip"],
        "teaching_tip_flow",
        duration=1000,
    )
