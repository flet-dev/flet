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
        ft.CupertinoCheckbox(),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_checked(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoCheckbox(
            value=True,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_label_position(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoCheckbox(
            label="Cupertino Checkbox with circle border",
            label_position=ft.LabelPosition.LEFT,
            value=True,
            shape=ft.CircleBorder(),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_label(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoCheckbox(
            label="Cupertino Checkbox with label",
        ),
    )
