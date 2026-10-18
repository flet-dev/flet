import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.tooltip.main as tooltip
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    # The tooltip opens in an overlay, so this is a full-page screenshot.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(260, 120)
    flet_app_function.page.add(
        ft.Container(
            padding=ft.Padding.only(top=50, left=40),
            content=shad.Tooltip(
                message="Add to library",
                content=shad.Button("Hover me", variant=shad.ButtonVariant.OUTLINE),
            ),
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.mouse_hover(
        await flet_app_function.tester.find_by_text("Hover me")
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
    [{"flet_app_main": tooltip.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 160)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Add to library")).count == 0
    await flet_app_function.tester.mouse_hover(
        await flet_app_function.tester.find_by_text("Hover me")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Add to library")).count == 1
    flet_app_function.assert_screenshot(
        "tooltip",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
