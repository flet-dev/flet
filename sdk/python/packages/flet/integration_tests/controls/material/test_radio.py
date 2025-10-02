import pytest

import flet as ft
import flet.testing as ftt

rg = ft.RadioGroup(
    content=ft.Column(
        controls=[
            ft.Radio(value="one", label="One"),
            ft.Radio(value="two", label="Two"),
            ft.Radio(value="three", label="Three"),
        ],
    ),
    value="one",
)


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_one(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(request.node.name, rg)


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_three(flet_app: ftt.FletTestApp, request):
    rg.value = "two"
    await flet_app.assert_control_screenshot(request.node.name, rg)
