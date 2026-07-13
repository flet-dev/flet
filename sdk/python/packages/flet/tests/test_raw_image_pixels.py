import asyncio

import pytest

import flet as ft
from flet.controls.core.raw_image import (
    RawImage,
    _encode_raw_packet,
    _premultiply_pil,
    _rgba_is_opaque,
)


def test_encode_raw_packet_layout():
    rgba = bytes(range(8))
    pkt = _encode_raw_packet(2, 1, rgba)
    assert pkt[0] == 0x04
    assert int.from_bytes(pkt[1:5], "little") == 2
    assert int.from_bytes(pkt[5:9], "little") == 1
    assert pkt[9:] == rgba
    assert len(pkt) == 9 + len(rgba)


def test_rgba_is_opaque():
    assert _rgba_is_opaque(b"")
    assert _rgba_is_opaque(b"\x01\x02\x03\xff" * 100)
    assert not _rgba_is_opaque(b"\x01\x02\x03\xff" * 99 + b"\x01\x02\x03\xfe")


def test_premultiply_pil_opaque_is_noop():
    PILImage = pytest.importorskip("PIL.Image")
    img = PILImage.new("RGBA", (4, 4), (10, 20, 30, 255))
    assert _premultiply_pil(img) is img


def test_premultiply_pil_matches_integer_math():
    PILImage = pytest.importorskip("PIL.Image")
    img = PILImage.new("RGBA", (1, 3))
    src = [(200, 100, 50, 128), (255, 255, 255, 0), (8, 16, 32, 255)]
    img.putdata(src)
    raw = _premultiply_pil(img).tobytes()
    out = [tuple(raw[i : i + 4]) for i in range(0, len(raw), 4)]
    for (r, g, b, a), (pr, pg, pb, pa) in zip(src, out):
        assert pa == a
        # ImageChops.multiply rounds a*b/255; allow off-by-one vs floor.
        for straight, pre in ((r, pr), (g, pg), (b, pb)):
            assert abs(pre - straight * a // 255) <= 1


def test_premultiply_pil_parity_with_numpy_math():
    PILImage = pytest.importorskip("PIL.Image")
    np = pytest.importorskip("numpy")
    rng = np.random.default_rng(7)
    arr = rng.integers(0, 256, size=(16, 16, 4), dtype=np.uint8)
    img = PILImage.frombuffer("RGBA", (16, 16), arr.tobytes())
    pil_out = np.frombuffer(_premultiply_pil(img).tobytes(), dtype=np.uint8)
    pil_out = pil_out.reshape(16, 16, 4).astype(np.int16)
    # The numpy premultiply used by the matplotlib Agg backend.
    a = arr[:, :, 3:4].astype(np.uint16)
    expected = arr.copy()
    expected[:, :, :3] = (arr[:, :, :3].astype(np.uint16) * a // 255).astype(np.uint8)
    assert np.abs(pil_out - expected.astype(np.int16)).max() <= 1


def test_array_packet_premultiplies_straight_alpha():
    np = pytest.importorskip("numpy")
    arr = np.zeros((1, 2, 4), dtype=np.uint8)
    arr[0, 0] = (200, 100, 50, 128)
    arr[0, 1] = (10, 20, 30, 255)
    pkt = RawImage._array_packet(np, arr, premultiplied=False)
    assert int.from_bytes(pkt[1:5], "little") == 2  # width
    assert int.from_bytes(pkt[5:9], "little") == 1  # height
    assert tuple(pkt[9:13]) == (
        200 * 128 // 255,
        100 * 128 // 255,
        50 * 128 // 255,
        128,
    )
    assert tuple(pkt[13:17]) == (10, 20, 30, 255)  # opaque pixel untouched


def test_array_packet_opaque_frame_is_passthrough():
    np = pytest.importorskip("numpy")
    arr = np.full((2, 2, 4), 255, dtype=np.uint8)
    arr[:, :, :3] = 42
    pkt = RawImage._array_packet(np, arr, premultiplied=False)
    assert pkt[9:] == arr.tobytes()


def test_render_rejects_unknown_input():
    ri = ft.RawImage()

    async def run():
        with pytest.raises(TypeError, match="PIL.Image.Image"):
            await ri.render("not an image")

    asyncio.run(run())


def test_render_rgba_rejects_wrong_length():
    ri = ft.RawImage()

    async def run():
        with pytest.raises(ValueError, match="width \\* height \\* 4"):
            await ri.render_rgba(2, 2, b"\x00" * 15)

    asyncio.run(run())


class _SilentChannel:
    """A channel that accepts frames but never acks — a dead client."""

    def __init__(self):
        self.sent = []

    def send(self, payload: bytes) -> None:
        self.sent.append(payload)


def test_render_times_out_without_ack():
    ri = ft.RawImage(ack_timeout=0.05)

    async def run():
        ri._channel = _SilentChannel()
        ri._ready.set()
        with pytest.raises(TimeoutError, match="not acknowledged"):
            await ri.render_rgba(1, 1, b"\x00\x00\x00\xff")
        # The abandoned future is withdrawn so a late ack can't resolve
        # the wrong frame's wait.
        assert not ri._pending_acks
        assert len(ri._channel.sent) == 1

    asyncio.run(run())
