import math

import flet as ft
import flet.canvas as fc
import flet.testing as ftt
import pytest


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_line(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [fc.Line(10, 10, 90, 90, ft.Paint(stroke_width=3))],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_line(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Line(
                    10,
                    10,
                    90,
                    90,
                    ft.Paint(
                        stroke_width=3, stroke_dash_pattern=[5, 5], color=ft.Colors.RED
                    ),
                )
            ],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_circle(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Circle(
                    x=50,
                    y=50,
                    radius=40,
                    paint=ft.Paint(stroke_width=3, style=ft.PaintingStyle.STROKE),
                )
            ],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_circle(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Circle(
                    x=50,
                    y=50,
                    radius=40,
                    paint=ft.Paint(
                        stroke_width=3,
                        stroke_dash_pattern=[5, 15],
                        color=ft.Colors.GREEN,
                        style=ft.PaintingStyle.STROKE,
                    ),
                )
            ],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_filled_circle_default_paint(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [fc.Circle(x=50, y=50, radius=40, paint=ft.Paint())],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_oval(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Oval(
                    x=10,
                    y=10,
                    width=90,
                    height=40,
                    paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE),
                )
            ],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_oval(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Oval(
                    x=10,
                    y=10,
                    width=90,
                    height=40,
                    paint=ft.Paint(
                        stroke_width=2,
                        stroke_dash_pattern=[5, 15],
                        color=ft.Colors.GREEN,
                        style=ft.PaintingStyle.STROKE,
                    ),
                )
            ],
            width=100,
            height=100,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_arc(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Arc(
                    40,
                    40,
                    100,
                    60,
                    math.pi * 0.1,
                    math.pi * 0.4,
                    paint=ft.Paint(
                        color=ft.Colors.YELLOW,
                        stroke_width=4,
                        style=ft.PaintingStyle.STROKE,
                    ),
                )
            ],
            width=200,
            height=150,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_arc(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Arc(
                    40,
                    40,
                    100,
                    60,
                    math.pi * 0.1,
                    math.pi * 0.4,
                    paint=ft.Paint(
                        color=ft.Colors.AMBER,
                        stroke_width=4,
                        stroke_dash_pattern=[7, 7],
                        style=ft.PaintingStyle.STROKE,
                    ),
                    use_center=False,
                )
            ],
            width=200,
            height=150,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_arc_with_center(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Arc(
                    x=40,
                    y=40,
                    width=100,
                    height=60,
                    start_angle=math.pi * 0.1,
                    sweep_angle=math.pi * 0.6,
                    paint=ft.Paint(
                        color=ft.Colors.AMBER,
                        stroke_width=4,
                        stroke_dash_pattern=[7, 7],
                        style=ft.PaintingStyle.STROKE,
                    ),
                    use_center=True,
                )
            ],
            width=200,
            height=150,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_filled_rect(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Rect(
                    x=40,
                    y=40,
                    width=100,
                    height=60,
                    border_radius=5,
                    paint=ft.Paint(
                        color=ft.Colors.AMBER,
                        stroke_width=4,
                    ),
                )
            ],
            width=200,
            height=150,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_rect(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Rect(
                    x=40,
                    y=40,
                    width=100,
                    height=60,
                    border_radius=5,
                    paint=ft.Paint(
                        color=ft.Colors.BLUE,
                        stroke_width=4,
                        stroke_dash_pattern=[3, 3],
                        style=ft.PaintingStyle.STROKE,
                    ),
                )
            ],
            width=200,
            height=150,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_flet_logo_with_path(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Path(
                    elements=[
                        fc.Path.MoveTo(25, 125),
                        fc.Path.QuadraticTo(50, 25, 135, 35, 0.35),
                        fc.Path.QuadraticTo(75, 115, 135, 215, 0.6),
                        fc.Path.QuadraticTo(50, 225, 25, 125, 0.35),
                    ],
                    paint=ft.Paint(
                        stroke_width=2,
                        style=ft.PaintingStyle.FILL,
                        color=ft.Colors.PINK_400,
                    ),
                ),
                fc.Path(
                    elements=[
                        fc.Path.MoveTo(85, 125),
                        fc.Path.QuadraticTo(120, 85, 165, 75, 0.5),
                        fc.Path.QuadraticTo(120, 115, 165, 175, 0.3),
                        fc.Path.QuadraticTo(120, 165, 85, 125, 0.5),
                    ],
                    paint=ft.Paint(
                        stroke_width=2,
                        style=ft.PaintingStyle.FILL,
                        color=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_400),
                    ),
                ),
            ],
            width=300,
            height=300,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_dashed_path_with_fill(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Fill(
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        gradient=ft.PaintLinearGradient(
                            begin=(0, 10),
                            end=(100, 50),
                            colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
                        ),
                    )
                ),
                fc.Path(
                    paint=ft.Paint(
                        stroke_width=3,
                        stroke_dash_pattern=[3, 3],
                        style=ft.PaintingStyle.STROKE,
                    ),
                    elements=[
                        fc.Path.MoveTo(75, 25),
                        fc.Path.QuadraticTo(25, 25, 25, 62.5),
                        fc.Path.QuadraticTo(25, 100, 50, 100),
                        fc.Path.QuadraticTo(50, 120, 30, 125),
                        fc.Path.QuadraticTo(60, 120, 65, 100),
                        fc.Path.QuadraticTo(125, 100, 125, 62.5),
                        fc.Path.QuadraticTo(125, 25, 75, 25),
                    ],
                ),
            ],
            width=150,
            height=150,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_text(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Fill(
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        color=ft.Colors.WHITE,
                    )
                ),
                fc.Text(
                    x=0,
                    y=0,
                    value="Just a text",
                ),
                fc.Circle(
                    x=200,
                    y=100,
                    radius=2,
                    paint=ft.Paint(color=ft.Colors.RED),
                ),
                fc.Text(
                    x=200,
                    y=100,
                    style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=30),
                    alignment=ft.Alignment.TOP_CENTER,
                    rotate=math.pi * 0.15,
                    value="Rotated",
                    spans=[
                        ft.TextSpan(
                            text="around top_center",
                            style=ft.TextStyle(
                                italic=True, color=ft.Colors.GREEN, size=20
                            ),
                        )
                    ],
                ),
                fc.Circle(
                    x=400,
                    y=100,
                    radius=2,
                    paint=ft.Paint(color=ft.Colors.RED),
                ),
                fc.Text(
                    x=400,
                    y=100,
                    value="Rotated around top_left",
                    style=ft.TextStyle(size=20),
                    alignment=ft.Alignment.TOP_LEFT,
                    rotate=math.pi * -0.15,
                ),
                fc.Circle(
                    x=600,
                    y=200,
                    radius=2,
                    paint=ft.Paint(color=ft.Colors.RED),
                ),
                fc.Text(
                    x=600,
                    y=200,
                    value="Rotated around center",
                    style=ft.TextStyle(size=20),
                    alignment=ft.Alignment.CENTER,
                    rotate=math.pi / 2,
                ),
                fc.Text(
                    x=300,
                    y=400,
                    value="Limited to max_width and right-aligned.\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                    text_align=ft.TextAlign.RIGHT,
                    max_width=400,
                ),
                fc.Text(
                    x=200,
                    y=200,
                    value="WOW!",
                    style=ft.TextStyle(
                        weight=ft.FontWeight.BOLD,
                        size=100,
                        foreground=ft.Paint(
                            color=ft.Colors.PINK,
                            stroke_width=6,
                            style=ft.PaintingStyle.STROKE,
                            stroke_join=ft.StrokeJoin.ROUND,
                            stroke_cap=ft.StrokeCap.ROUND,
                        ),
                    ),
                ),
                fc.Text(
                    x=200,
                    y=200,
                    value="WOW!",
                    style=ft.TextStyle(
                        weight=ft.FontWeight.BOLD,
                        size=100,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                begin=(200, 200),
                                end=(300, 300),
                                colors=[ft.Colors.YELLOW, ft.Colors.RED],
                            ),
                            stroke_join=ft.StrokeJoin.ROUND,
                            stroke_cap=ft.StrokeCap.ROUND,
                        ),
                    ),
                ),
            ],
            width=800,
            height=500,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_gradients(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [
                fc.Rect(
                    x=10,
                    y=10,
                    width=100,
                    height=100,
                    border_radius=5,
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        gradient=ft.PaintLinearGradient(
                            begin=(0, 10),
                            end=(100, 50),
                            colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
                        ),
                    ),
                ),
                fc.Circle(
                    x=60,
                    y=170,
                    radius=50,
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        gradient=ft.PaintRadialGradient(
                            radius=50,
                            center=(60, 170),
                            colors=[ft.Colors.YELLOW, ft.Colors.BLUE],
                        ),
                    ),
                ),
                fc.Path(
                    elements=[
                        fc.Path.Arc(
                            x=10,
                            y=230,
                            width=100,
                            height=100,
                            start_angle=3 * math.pi / 4,
                            sweep_angle=3 * math.pi / 2,
                        ),
                    ],
                    paint=ft.Paint(
                        stroke_width=15,
                        stroke_join=ft.StrokeJoin.ROUND,
                        style=ft.PaintingStyle.STROKE,
                        gradient=ft.PaintSweepGradient(
                            start_angle=0,
                            end_angle=math.pi * 2,
                            rotation=3 * math.pi / 4,
                            center=(60, 280),
                            colors=[ft.Colors.YELLOW, ft.Colors.PURPLE],
                            color_stops=[0.0, 1.0],
                        ),
                    ),
                ),
            ],
            width=150,
            height=350,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_asset_image(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [fc.Image(src="52-100x100.png", x=10, y=10)],
            width=120,
            height=120,
        ),
        pump_times=1,
        pump_duration=1000,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_draw_url_image(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        fc.Canvas(
            [fc.Image(src="https://picsum.photos/id/237/100/100", x=10, y=10)],
            width=120,
            height=120,
        ),
        pump_times=7,
        pump_duration=1000,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_capture(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    canvas = fc.Canvas(
        [
            fc.Circle(
                x=50,
                y=50,
                radius=40,
                paint=ft.Paint(
                    stroke_width=3,
                    color=ft.Colors.GREEN,
                    style=ft.PaintingStyle.STROKE,
                ),
            )
        ],
        width=100,
        height=100,
    )
    screenshot = ft.Screenshot(canvas)

    # clean page
    flet_app.page.clean()
    await flet_app.tester.pump_and_settle()

    # add canvas to a page, pump and settle
    flet_app.page.add(screenshot)
    await flet_app.tester.pump_and_settle()

    # ensure there is no initial capture
    capture_0 = await canvas.get_capture_async()
    assert capture_0 is None

    # take capture and assert
    await canvas.capture_async(pixel_ratio=flet_app.pixel_ratio)
    capture_1 = await canvas.get_capture_async()
    assert capture_1 is not None
    flet_app.assert_screenshot("capture_1", capture_1)

    # clean canvas and draw a line
    canvas.shapes = [fc.Line(10, 10, 90, 90, ft.Paint(stroke_width=3))]
    canvas.update()
    await flet_app.tester.pump_and_settle()

    # take screenshot
    # it must be a circle striked out with a line (capture + shapes)
    capture_2 = await screenshot.capture_async(pixel_ratio=flet_app.pixel_ratio)
    flet_app.assert_screenshot("capture_2", capture_2)

    # clean current capture
    await canvas.clear_capture_async()
    await flet_app.tester.pump_and_settle()

    # take screenshot
    # it must be just a single line
    capture_3 = await screenshot.capture_async(pixel_ratio=flet_app.pixel_ratio)
    flet_app.assert_screenshot("capture_3", capture_3)

    # back to empty capture
    capture_4 = await canvas.get_capture_async()
    assert capture_4 is None
