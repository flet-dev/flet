import base64

import pytest

import flet as ft
import flet.testing as ftt

base64_image = "iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"  # noqa: E501


@pytest.mark.asyncio(loop_scope="module")
async def test_src_png(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="/minion.png",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
        ),
        pump_times=1,
        pump_duration=1000,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_src_base64(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src=base64_image,
            width=100,
            height=100,
        ),
        pump_times=1,
        pump_duration=1000,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_src_svg_url(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="https://flet.dev/img/logo.svg",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
        ),
        pump_times=5,
        pump_duration=1000,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_src_svg_string(flet_app: ftt.FletTestApp, request):
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
    <g transform="matrix(0.99491265,0,0,0.99491265,11.874769,605.3797)">
    <path fill="#27b0f5" d="m 200.63848,-393.81653 c -9.17235,-9.55307 -9.17235,-17.71898 0,-27.27205 C 226.84523,-448.38309 266,-482 330,-502 c 9.96506,-3.11408 15.90008,4.63778 14,14 -6.54846,32.26605 -10.418,56.47549 -10.68635,80.54744 0.26835,24.07196 4.13789,48.2814 10.68635,80.54745 1.90008,9.36222 -4.03494,17.11408 -14,14 -64,-20 -103.15477,-53.61691 -129.36152,-80.91142 z"/>
    <path fill="#ff005f" d="m 45.577922,-378.88272 c -15.674995,-21.42738 -15.674995,-35.71229 0,-57.13967 C 61.25304,-457.44974 120,-537.41553 252,-605 c 20.9287,-10.71557 32.80454,5.54729 28,19 -22.76937,63.75424 -34.01776,120.85191 -33.74516,178.54744 -0.2726,57.69554 10.97579,114.79321 33.74516,178.54745 4.80454,13.45271 -7.0713,29.71557 -28,19 C 120,-277.48958 61.25304,-357.45537 45.577922,-378.88272 Z"/>
    <path fill="#8c0075" d="m 199.45908,-395.44598 c -7.59976,-8.41314 -7.59976,-15.60001 0,-24.01315 12.56302,-13.90733 50.05781,-43.72203 50.05781,-43.72203 -2.1637,18.27023 -3.20379,37.0672 -3.13658,55.7286 -0.0672,18.66141 0.97288,37.45838 3.13658,55.72861 0,0 -37.49479,-29.8147 -50.05781,-43.72203 z"/>
    </g>
    </svg>
    """  # noqa: E501

    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src=svg,
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
        ),
        pump_times=1,
        pump_duration=1000,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_src_bytes(flet_app: ftt.FletTestApp, request):
    # Decode the Base64 string into bytes
    bytes_image = base64.b64decode(base64_image)

    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src=bytes_image,
            width=100,
            height=100,
        ),
        pump_times=1,
        pump_duration=1000,
    )


@pytest.mark.skip(reason="The test is flaky on CI")
@pytest.mark.asyncio(loop_scope="module")
async def test_placeholder_1(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="/minion.png",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
            placeholder_src=base64_image,
            fade_in_animation=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
            placeholder_fade_out_animation=ft.Animation(
                250, ft.AnimationCurve.EASE_OUT
            ),
        ),
        pump_times=1,
        pump_duration=50,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_placeholder_2(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="/minion.png",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
            placeholder_src=base64_image,
            fade_in_animation=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
            placeholder_fade_out_animation=ft.Animation(
                250, ft.AnimationCurve.EASE_OUT
            ),
        ),
        pump_times=3,
        pump_duration=1000,
    )
