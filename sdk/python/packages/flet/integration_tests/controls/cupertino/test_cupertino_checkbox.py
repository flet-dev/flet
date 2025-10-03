import pytest

import flet as ft
import flet.testing as ftt

ccbts = ft.CupertinoCheckbox(
    label="Cupertino Checkbox tristate",
    value=True,
    tristate=True,
    check_color=ft.Colors.GREY_900,
    fill_color={
        ft.ControlState.SELECTED: ft.Colors.DEEP_ORANGE_200,
        ft.ControlState.DEFAULT: ft.Colors.TEAL_200,
    },
    key="tristate",
)

ccb = ft.CupertinoCheckbox(
    label="Cupertino Checkbox circle border",
    value=True,
    shape=ft.CircleBorder(),
    key="circleborder",
)


@pytest.mark.asyncio(loop_scope="module")
async def test_tristate_1(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ccbts,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_tristate_2(flet_app: ftt.FletTestApp, request):
    ccbts.value = None
    await flet_app.assert_control_screenshot(
        request.node.name,
        ccbts,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ccb,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_position(flet_app: ftt.FletTestApp, request):
    ccb.label_position = ft.LabelPosition.LEFT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ccb,
    )
