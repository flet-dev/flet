import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.TextField(margin=20),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_label(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.TextField(label="TextField label", margin=20),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_with_label_and_value(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.TextField(label="TextField label", value="TextField 1 value", margin=20),
    )
