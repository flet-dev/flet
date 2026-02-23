import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT

    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="https://flet.dev/img/logo.svg",
            width=100,
            height=100,
        ),
        pump_times=3,
        pump_duration=1000,
    )

@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.timeout(40)
@pytest.mark.parametrize(
    "flet_app_function",
    [{"skip_pump_and_settle": True}],
    indirect=True,
)
async def test_image_broken_source_fails_fast(
    flet_app_function: ftt.FletTestApp, request
):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT

    with pytest.raises(RuntimeError, match="Golden image .* not found"):
        await flet_app_function.assert_control_screenshot(
            request.node.name,
            ft.Image(
                src="https://flet.dev/this-image-does-not-exist-404.png",
                width=100,
                height=100,
            ),
        )
