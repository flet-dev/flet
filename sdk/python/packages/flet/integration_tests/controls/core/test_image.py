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
    <svg xmlns="http://www.w3.org/2000/svg" width="396" height="510" viewBox="0 0 396.46747 510">
    <g transform="matrix(1.7561529,0,0,1.7561529,-123.64424,-1000.5225)">
    <g transform="matrix(0.88898496,0,0,0.88898496,-903.09959,1089.086)">
    <path fill="#27b0f5" d="m 1231.3122,-409.73702 c -7.4909,-7.80181 -7.4909,-14.48913 0,-22.29095 21.4026,-22.29096 53.5071,-50.15464 107.0139,-66.87286 7.4907,0 10.7012,3.34365 10.7012,11.1455 -12.3338,52.97014 -15.2054,81.27375 0,133.74567 0,8.0191 -3.0016,11.14548 -10.7012,11.14548 -53.5068,-16.71821 -85.6113,-44.5819 -107.0139,-66.87284 z"/>
    <path fill="#ff005f" d="m 1104.6769,-444.22416 c 12.8016,-17.49935 64.0079,-87.49683 172.822,-139.99492 19.2022,0 19.2022,5.83312 19.2022,17.49936 -38.4047,99.16308 -38.4047,192.49303 0,291.65612 0,10.08688 0,17.94809 -19.2022,17.49937 -102.413,-46.66497 -160.0204,-122.49558 -172.822,-139.99494 -12.8015,-17.49938 -12.8015,-29.16562 0,-46.66499 z"/>
    <path fill="#8c0075" d="m 1230.349,-430.69723 c -6.2066,6.87087 -6.2066,12.76018 0,19.63108 10.2598,11.35788 22.4747,23.67747 40.3877,35.46954 -3.7777,-30.37498 -3.7369,-62.29377 -0.017,-90.52898 0,0 -30.1107,24.07048 -40.3705,35.42836 z"/>
    </g>
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
