from math import pi

import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_flip(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=220,
            height=120,
            bgcolor=ft.Colors.BLUE_300,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Flip", size=28, weight=ft.FontWeight.BOLD),
            flip=ft.Flip(
                flip_x=True,
                flip_y=True,
                filter_quality=ft.FilterQuality.MEDIUM,
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_rotate(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=220,
            height=120,
            bgcolor=ft.Colors.BLUE_300,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Rotate", size=28, weight=ft.FontWeight.BOLD),
            rotate=ft.Rotate(
                angle=pi / 10,
                alignment=ft.Alignment.CENTER,
                filter_quality=ft.FilterQuality.MEDIUM,
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_scale(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=220,
            height=120,
            bgcolor=ft.Colors.GREEN_300,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Scale", size=28, weight=ft.FontWeight.BOLD),
            scale=ft.Scale(
                scale_x=1.18,
                scale_y=0.82,
                alignment=ft.Alignment.CENTER,
                filter_quality=ft.FilterQuality.MEDIUM,
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_offset(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Stack(
            width=460,
            height=260,
            controls=[
                ft.Text(
                    "Offset translates by control size.",
                    left=12,
                    top=8,
                    size=16,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Container(
                    left=30,
                    top=70,
                    width=170,
                    height=90,
                    border_radius=16,
                    bgcolor=ft.Colors.BLUE_100,
                    border=ft.Border.all(2, ft.Colors.BLUE_GREY_400),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Original", size=20, color=ft.Colors.BLUE_GREY_700),
                ),
                ft.Container(
                    left=30,
                    top=70,
                    width=170,
                    height=90,
                    border_radius=16,
                    bgcolor=ft.Colors.AMBER_300,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Offset", size=26, weight=ft.FontWeight.BOLD),
                    offset=ft.Offset(
                        x=1.05,
                        y=0.55,
                        filter_quality=ft.FilterQuality.MEDIUM,
                    ),
                ),
                ft.Icon(
                    ft.Icons.ARROW_RIGHT_ALT_ROUNDED,
                    left=212,
                    top=82,
                    size=44,
                    color=ft.Colors.BLUE_GREY_600,
                ),
                ft.Text(
                    "offset = Offset(1.05, 0.55)",
                    left=194,
                    top=222,
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
        ),
    )


def _matrix_card(title: str, color: str, matrix: ft.Matrix4) -> ft.Container:
    return ft.Container(
        width=220,
        height=130,
        border_radius=18,
        bgcolor=color,
        padding=12,
        content=ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
        transform=ft.Transform(
            matrix=matrix,
            alignment=ft.Alignment.CENTER,
            filter_quality=ft.FilterQuality.MEDIUM,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_matrix4_perspective_tilt(flet_app: ftt.FletTestApp, request):
    matrix = (
        ft.Matrix4.identity()
        .set_entry(3, 2, 0.0018)
        .rotate_x(-0.35)
        .rotate_y(0.45)
        .translate(0, -10, 0)
    )

    await flet_app.assert_control_screenshot(
        request.node.name,
        _matrix_card("Perspective tilt", ft.Colors.CYAN_300, matrix),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_matrix4_skew_and_rotate(flet_app: ftt.FletTestApp, request):
    matrix = ft.Matrix4.skew_y(0.28).rotate_z(-pi / 14)

    await flet_app.assert_control_screenshot(
        request.node.name,
        _matrix_card("Skew + rotate", ft.Colors.AMBER_300, matrix),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_matrix4_mirrored_spin(flet_app: ftt.FletTestApp, request):
    matrix = ft.Matrix4.diagonal3_values(-1, 1, 1).rotate_z(pi / 10)

    await flet_app.assert_control_screenshot(
        request.node.name,
        _matrix_card("Mirror + spin", ft.Colors.PINK_200, matrix),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_matrix4_multiply_chain(flet_app: ftt.FletTestApp, request):
    matrix = ft.Matrix4.translation_values(24, -8, 0).multiply(
        ft.Matrix4.rotation_z(pi / 16).scale(0.9, 0.9)
    )

    await flet_app.assert_control_screenshot(
        request.node.name,
        _matrix_card("Multiply chain", ft.Colors.LIGHT_GREEN_300, matrix),
    )
