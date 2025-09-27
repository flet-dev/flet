import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_standard(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_standard_disabled(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(ft.Icons.HOME, disabled=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_standard_selected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(ft.Icons.HOME, selected=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_standard_unselected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(ft.Icons.HOME, selected=False),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_disabled(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledIconButton(ft.Icons.HOME, disabled=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_selected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledIconButton(ft.Icons.HOME, selected=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_unselected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledIconButton(ft.Icons.HOME, selected=False),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_tonal(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledTonalIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_tonal_disabled(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledTonalIconButton(ft.Icons.HOME, disabled=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_tonal_selected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledTonalIconButton(ft.Icons.HOME, selected=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_tonal_unselected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledTonalIconButton(ft.Icons.HOME, selected=False),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_outlined(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.OutlinedIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_outlined_disabled(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.OutlinedIconButton(ft.Icons.HOME, disabled=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_outlined_selected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.OutlinedIconButton(ft.Icons.HOME, selected=True),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_outlined_unselected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.OutlinedIconButton(ft.Icons.HOME, selected=False),
    )
