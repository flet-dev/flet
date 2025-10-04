import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.checkbox import (
    basic,
    styled,
)


@pytest.mark.asyncio(loop_scope="module")
async def test_image_for_docs(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[
                ft.Checkbox(),
                ft.Checkbox(label="Checked", value=True),
                ft.Checkbox(label="Disabled", disabled=True),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": styled.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_content(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "styled_checkboxes",
        await flet_app_function.take_page_controls_screenshot(),
    )
