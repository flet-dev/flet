import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Slider(value=0.3),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_range_and_label(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Slider(min=0, max=100, divisions=10, label="{value}%"),
    )
