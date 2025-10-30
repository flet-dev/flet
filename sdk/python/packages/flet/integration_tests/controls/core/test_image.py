import base64

import pytest

import flet as ft
import flet.testing as ftt

base64_string = "iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"  # noqa: E501


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
            src_base64=base64_string,
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
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <!-- Creator: CorelDRAW 2017 -->
    <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="307px" height="307px" version="1.1" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd"
    viewBox="0 0 285 285"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <g id="Layer_x0020_1">
    <metadata id="CorelCorpID_0Corel-Layer"/>
    <rect fill="none" width="285" height="285" rx="9.03" ry="8.12"/>
    <path fill="#EE3167" d="M39.28 144.74c-0.85,-1.52 -0.66,-2.61 0.1,-4.13 31.41,-58.36 78.81,-94.15 138.53,-119.75 2.03,-0.86 5.04,1.52 4.31,3.65 -8.9,25.91 -15.18,51.13 -18.82,78.23 -3.32,24.97 -4.24,50.79 -0.87,77.77 3.56,30.59 10.88,55.99 19.68,83.36 0.98,3.05 -2.14,4.43 -4.51,3.26 -62.19,-30.61 -109.33,-70.65 -138.42,-122.39z"/>
    <path fill="#0098DA" fill-opacity="0.639216" d="M224.53 198.59c-34.39,-10.79 -65.15,-29.06 -92.4,-53.2 -1.82,-1.62 -1.61,-3.87 0.03,-5.44 27.07,-25.88 57.79,-46.19 91.74,-60.56 2.99,-1.27 5.45,1.2 4.56,4.62 -9.62,36.91 -11.74,73.39 0.13,109.95 0.98,3.05 -1.47,5.44 -4.06,4.63z"/>
    <path fill="#5ABAE7" d="M224.53 198.59c-22.64,-7.1 -43.71,-17.45 -63.24,-30.58 -1.35,-20.9 -1.47,-30.2 0.73,-53.26 19.19,-14.22 39.86,-26.04 61.88,-35.36 2.99,-1.27 5.45,1.2 4.56,4.62 -9.62,36.91 -11.74,73.39 0.13,109.95 0.98,3.05 -1.47,5.44 -4.06,4.63z"/>
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
@pytest.mark.skip(reason="image is not rendered from src_bytes in CI environment")
async def test_src_bytes(flet_app: ftt.FletTestApp, request):
    # Decode the Base64 string into bytes
    image_bytes = base64.b64decode(base64_string)

    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src_bytes=image_bytes,
            width=100,
            height=100,
        ),
        pump_times=1,
        pump_duration=1000,
    )
