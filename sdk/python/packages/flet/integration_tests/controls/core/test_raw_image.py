import io
from pathlib import Path
from typing import Optional

import pytest

import flet as ft
import flet.testing as ftt

assets_dir = Path(__file__).resolve().parent / "../../assets"


def gradient_rgba(width: int, height: int) -> bytes:
    """
    A deterministic opaque test pattern: red rises left to right,
    green top to bottom, constant blue.
    """
    pixels = bytearray(width * height * 4)
    i = 0
    for y in range(height):
        g = y * 255 // (height - 1)
        for x in range(width):
            pixels[i] = x * 255 // (width - 1)
            pixels[i + 1] = g
            pixels[i + 2] = 64
            pixels[i + 3] = 255
            i += 4
    return bytes(pixels)


async def show_raw_image(
    flet_app: ftt.FletTestApp,
    raw_image: ft.RawImage,
    host: Optional[ft.Control] = None,
) -> ft.Screenshot:
    """
    Puts `raw_image` (or `host` containing it) on a clean page, wrapped in
    a Screenshot, and waits for the widget to mount and open its data
    channel so subsequent `render` calls can complete.
    """
    flet_app.page.clean()
    await flet_app.tester.pump_and_settle()
    screenshot = ft.Screenshot(host or raw_image)
    flet_app.page.add(screenshot)
    await flet_app.tester.pump_and_settle()
    return screenshot


async def assert_raw_image_screenshot(
    flet_app: ftt.FletTestApp, name: str, screenshot: ft.Screenshot
):
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        name,
        await screenshot.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_render_rgba(flet_app: ftt.FletTestApp, request):
    ri = ft.RawImage(width=100, height=80)
    screenshot = await show_raw_image(flet_app, ri)
    await ri.render_rgba(100, 80, gradient_rgba(100, 80))
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_render_pil_alpha(flet_app: ftt.FletTestApp, request):
    PILImage = pytest.importorskip("PIL.Image")
    from PIL import ImageDraw

    # A semi-transparent white disc: correct premultiplication shows an
    # evenly lightened green circle; skipping it would wash out the whole
    # square (straight-alpha values uploaded as premultiplied read too
    # bright).
    img = PILImage.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 90, 90), fill=(255, 255, 255, 128))

    ri = ft.RawImage(width=100, height=100)
    screenshot = await show_raw_image(
        flet_app,
        ri,
        host=ft.Container(ri, bgcolor=ft.Colors.GREEN, padding=10),
    )
    await ri.render(img)
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_render_encoded(flet_app: ftt.FletTestApp, request):
    PILImage = pytest.importorskip("PIL.Image")
    buf = io.BytesIO()
    PILImage.frombuffer("RGBA", (100, 80), gradient_rgba(100, 80)).save(
        buf, format="PNG"
    )

    ri = ft.RawImage(width=100, height=80)
    screenshot = await show_raw_image(flet_app, ri)
    await ri.render_encoded(buf.getvalue())
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_render_encoded_png_file(flet_app: ftt.FletTestApp, request):
    # A regular PNG file straight from disk — no Pillow involved.
    ri = ft.RawImage(width=100, height=100, fit=ft.BoxFit.CONTAIN)
    screenshot = await show_raw_image(flet_app, ri)
    await ri.render_encoded((assets_dir / "minion.png").read_bytes())
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_render_encoded_jpg_file(flet_app: ftt.FletTestApp, request):
    # A regular JPEG file straight from disk — no Pillow involved.
    ri = ft.RawImage(width=100, height=100, fit=ft.BoxFit.CONTAIN)
    screenshot = await show_raw_image(flet_app, ri)
    await ri.render_encoded((assets_dir / "141-50x50.jpg").read_bytes())
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_render_numpy_rgb(flet_app: ftt.FletTestApp, request):
    np = pytest.importorskip("numpy")
    # RGB input (no alpha channel) is padded to opaque RGBA.
    arr = np.zeros((60, 90, 3), dtype=np.uint8)
    arr[:30, :, 0] = 255
    arr[30:, :, 2] = 255

    ri = ft.RawImage(width=90, height=60)
    screenshot = await show_raw_image(flet_app, ri)
    await ri.render(arr)
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_fit_contain(flet_app: ftt.FletTestApp, request):
    # A 20x10 frame inscribed into a 100x100 box.
    ri = ft.RawImage(
        width=100,
        height=100,
        fit=ft.BoxFit.CONTAIN,
        filter_quality=ft.FilterQuality.NONE,
    )
    screenshot = await show_raw_image(
        flet_app,
        ri,
        host=ft.Container(ri, bgcolor=ft.Colors.BLUE_GREY_100),
    )
    await ri.render_rgba(20, 10, gradient_rgba(20, 10))
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_clear(flet_app: ftt.FletTestApp, request):
    ri = ft.RawImage(width=100, height=80)
    screenshot = await show_raw_image(
        flet_app,
        ri,
        host=ft.Container(ri, bgcolor=ft.Colors.AMBER_100),
    )
    await ri.render_rgba(100, 80, gradient_rgba(100, 80))
    await ri.clear()
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)


@pytest.mark.asyncio(loop_scope="module")
async def test_sequential_renders(flet_app: ftt.FletTestApp, request):
    # Backpressure round-trip: each render resolves on the client's ack,
    # so a burst of awaited renders must complete without deadlocking and
    # leave the last frame on screen.
    ri = ft.RawImage(width=100, height=80)
    screenshot = await show_raw_image(flet_app, ri)
    solid = bytes([0, 0, 255, 255]) * (100 * 80)
    for _ in range(3):
        await ri.render_rgba(100, 80, solid)
        await ri.render_rgba(100, 80, gradient_rgba(100, 80))
    await assert_raw_image_screenshot(flet_app, request.node.name, screenshot)
