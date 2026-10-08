import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.popover.main as popover
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    # The popover opens in an overlay, so this is a full-page screenshot.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 180)
    flet_app_function.page.add(
        shad.Popover(
            open=True,
            content=shad.Button("Open popover", variant=shad.ButtonVariant.OUTLINE),
            popover=ft.Text("Place content for the popover here."),
        )
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": popover.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_popover(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(380, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    async def capture(name: str):
        flet_app_function.assert_screenshot(
            name,
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            ),
        )

    await capture("popover_closed")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Open popover")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Dimensions")).count == 1
    await capture("popover_open")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Apply")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Dimensions")).count == 0
    assert (await flet_app_function.tester.find_by_text("Size: 100% x 25px")).count == 1
    await capture("popover")

    # Tapping outside closes it and reports on_dismiss.
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Open popover")
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap_at(ft.Offset(340, 380))
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Dimensions")).count == 0
    assert (
        await flet_app_function.tester.find_by_text("Closed by tapping outside")
    ).count == 1

    flet_app_function.create_gif(
        ["popover_closed", "popover_open", "popover"], "popover_flow", duration=1000
    )
