import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.input_otp.main as input_otp
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.InputOTP(value="123", length=6, groups=[3, 3]),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": input_otp.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_input_otp(flet_app_function: ftt.FletTestApp):
    # Each box is a separate text field, so the code is set from Python rather
    # than typed; Clear is then clicked like a user would.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    otp = next(c for c in _walk(flet_app_function.page) if isinstance(c, shad.InputOTP))
    otp.value = "123456"
    otp.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("6")).count == 1
    flet_app_function.assert_screenshot(
        "input_otp",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Clear")
    )
    await flet_app_function.tester.pump_and_settle()

    assert otp.value == ""
    assert (await flet_app_function.tester.find_by_text("6")).count == 0
    flet_app_function.assert_screenshot(
        "input_otp_cleared",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["input_otp", "input_otp_cleared"], "input_otp_flow", duration=1000
    )


def _walk(control):
    yield control
    for name in ("controls", "content"):
        child = getattr(control, name, None)
        for c in child if isinstance(child, list) else [child]:
            if isinstance(c, ft.BaseControl):
                yield from _walk(c)
