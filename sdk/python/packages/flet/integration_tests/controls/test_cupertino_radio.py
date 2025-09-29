import pytest

import flet as ft
import flet.testing as ftt

rs: list[ft.CupertinoRadio] = [
    ft.CupertinoRadio(
        value="red",
        label="Red",
        active_color=ft.Colors.RED_600,
        inactive_color=ft.Colors.RED_200,
        key="red",
    ),
    ft.CupertinoRadio(
        value="green",
        label="Green",
        fill_color=ft.Colors.GREEN,
        key="green",
    ),
    ft.CupertinoRadio(
        value="blue",
        label="Blue",
        active_color=ft.Colors.BLUE,
        key="blue",
    ),
]

rg = ft.RadioGroup(
    content=ft.Column(
        controls=rs,
    ),
    value="red",
)


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_red(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(request.node.name, rg)


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_blue(flet_app: ftt.FletTestApp, request):
    rg.value = "blue"
    await flet_app.assert_control_screenshot(
        request.node.name,
        rg,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_checkmark(flet_app: ftt.FletTestApp, request):
    for c in rs:
        c.use_checkmark_style = True
    rg.update()
    await flet_app.assert_control_screenshot(
        request.node.name,
        rg,
    )
