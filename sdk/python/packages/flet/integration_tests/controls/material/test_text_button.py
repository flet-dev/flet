import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.TextButton("Click me"),
    )
