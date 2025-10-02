import pytest

import flet as ft
import flet.testing as ftt

sw = ft.CupertinoSwitch(
    label="Cupertino Switch",
    value=True,
)


@pytest.mark.asyncio(loop_scope="module")
async def test_true(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        sw,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_false(flet_app: ftt.FletTestApp, request):
    sw.value = False
    await flet_app.assert_control_screenshot(
        request.node.name,
        sw,
    )
