import asyncio
import contextlib
import io
from collections import deque
from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.box import BoxFit, FilterQuality
from flet.controls.control_event import EventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import Number
from flet.data_channel import DataChannel, DataChannelOpenEvent

__all__ = ["RawImage"]


@control("RawImage")
class RawImage(LayoutControl):
    """
    Displays pixel frames pushed from Python at full bandwidth.

    Unlike :class:`~flet.Image`, whose `src` travels through the regular
    Flet protocol on every update, `RawImage` streams frames over a
    dedicated :class:`~flet.DataChannel`: bytes skip MsgPack
    encode/decode entirely and, on local transports (desktop app, `flet run`,
    Pyodide), are displayed from raw RGBA pixels without any image
    encoding or decoding. This makes it suitable for animations, generated
    graphics, camera frames and Pillow output at interactive frame rates.

    Frames are pushed with the awaitable :meth:`render`, :meth:`render_rgba`
    and :meth:`render_encoded` methods. Each call resolves when the client
    has actually displayed the frame, so a plain loop self-paces to display
    speed:

    ```python
    raw_image = ft.RawImage(width=400, height=300)
    page.add(raw_image)

    while True:
        await raw_image.render(produce_pil_image())
    ```

    Transport behavior is selected automatically:

    - **Local transports** (`local_data_transport` connections): frames are
      sent as uncompressed premultiplied RGBA8888 and uploaded straight to
      a GPU texture on the client.
    - **Remote transports** (`flet-web` over WebSocket): Pillow and NumPy
      frames are PNG-encoded off the event loop to save bandwidth; raw
      pixel frames for which no straight-alpha source is available are sent
      uncompressed.

    **Premultiplied alpha.** The raw-pixel path uploads frames directly as
    GPU textures in Flutter's `rgba8888` format, which expects RGB values
    already multiplied by alpha ("premultiplied"). Pillow, numpy code and
    image files normally produce *straight* alpha instead, where color and
    opacity are independent: a half-transparent white pixel is
    `(255, 255, 255, 128)` straight but `(128, 128, 128, 128)`
    premultiplied (each color channel becomes `value * alpha // 255`).
    The `premultiplied` argument of the render methods says whether that
    conversion is already done:

    - `premultiplied=False` — pixels carry straight alpha; RGB is
      multiplied by alpha before sending. The conversion runs in fast C
      loops and is skipped when the frame turns out to be fully opaque.
    - `premultiplied=True` — skip the conversion. Use it when pixels are
      genuinely premultiplied or, the common case, when the frame is
      **fully opaque**: with every alpha at 255 both forms are identical,
      and declaring it saves an alpha scan per frame in streaming loops.

    Passing straight-alpha pixels with `premultiplied=True` makes
    semi-transparent areas render too bright; for fully opaque frames the
    flag cannot be wrong either way.

    The last frame is retained and replayed automatically when the client
    widget remounts (page rebuild, route navigation), mirroring how
    `Image.src` persists.
    """

    fit: Optional[BoxFit] = None
    """
    Defines how to inscribe the current frame into the space allocated
    during layout.
    """

    filter_quality: FilterQuality = FilterQuality.LOW
    """
    The rendering quality of the displayed frame.

    Defaults to `LOW` (bilinear), a good trade-off for streamed frames.
    Use `NONE` for crisp nearest-neighbor scaling of pixel-art-style
    content.
    """

    scale: Number = 1.0
    """
    How many physical frame pixels correspond to one logical pixel.

    Only affects the intrinsic size of this control when it is laid out
    without tight constraints: a 800x600 frame with `scale=2` measures
    400x300 logical pixels. Set it to the device pixel ratio when frames
    are rendered at physical resolution.
    """

    ready_timeout: Optional[Number] = 5.0
    """
    Seconds the `render` methods wait for the client widget to attach its
    data channel before raising `TimeoutError`.

    Set to `None` to wait indefinitely.
    """

    ack_timeout: Optional[Number] = 10.0
    """
    Seconds a `render` call waits for the client's frame-applied
    acknowledgment before raising `TimeoutError`.

    The ack normally arrives within milliseconds of the frame being
    displayed. The timeout is a liveness guard: transports drop frames
    sent while the client is disconnected (closed browser tab, network
    loss), and without it a `while True: await raw_image.render(...)`
    loop would wait for the lost ack forever. Raise it when streaming
    very large frames to slow remote clients, or set to `None` to wait
    indefinitely.
    """

    on_data_channel_open: Optional[EventHandler[DataChannelOpenEvent]] = None
    """
    Framework hook — Dart fires this when it opens the data channel on
    mount. The default handler captures the channel used by the `render`
    methods; override only to do something extra at attach-time.
    """

    def init(self) -> None:
        super().init()
        self._channel: Optional[DataChannel] = None
        # Set once the Dart side has announced its data channel; `render`
        # calls block on it so frames pushed before first mount are held
        # (up to `ready_timeout`) instead of dropped.
        self._ready = asyncio.Event()
        # FIFO of per-frame ack futures. Each send enqueues a future and
        # awaits it; `_on_dart_message` resolves the head when Dart's
        # `[0xFF]` frame-applied ack arrives. The await is the
        # backpressure that paces producer loops to display speed.
        self._pending_acks: deque[asyncio.Future] = deque()
        # Last frame packet sent, replayed when the client widget
        # remounts so the image survives page rebuilds like `Image.src`.
        self._last_packet: Optional[bytes] = None
        if self.on_data_channel_open is None:
            self.on_data_channel_open = self._capture_channel

    # -- channel plumbing ---------------------------------------------------

    def _capture_channel(self, e: DataChannelOpenEvent) -> None:
        # Single-channel widget; no need to dispatch on e.channel_name.
        self._channel = self.get_data_channel(e.channel_id)
        self._channel.on_bytes(self._on_dart_message)
        # Acks pending on a previous channel will never arrive; resolve
        # them so old `render` awaits return instead of hanging.
        while self._pending_acks:
            fut = self._pending_acks.popleft()
            if not fut.done():
                fut.set_result(None)
        # Replay the last frame without registering an ack future — its
        # ack finds an empty deque and is ignored.
        if self._last_packet is not None:
            self._channel.send(self._last_packet)
        self._ready.set()

    def _on_dart_message(self, payload: bytes) -> None:
        # Reverse direction (Dart -> Python) wire format:
        #   [0xFF] — frame-applied ack, sent after each frame completes.
        if not payload or payload[0] != 0xFF:
            return
        if self._pending_acks:
            fut = self._pending_acks.popleft()
            if not fut.done():
                fut.set_result(None)

    async def _send_and_wait(self, packet: bytes) -> None:
        if not self._ready.is_set():
            await asyncio.wait_for(
                self._ready.wait(),
                None if self.ready_timeout is None else float(self.ready_timeout),
            )
        assert self._channel is not None
        loop = asyncio.get_running_loop()
        fut: asyncio.Future = loop.create_future()
        self._pending_acks.append(fut)
        self._channel.send(packet)
        if self.ack_timeout is None:
            await fut
            return
        try:
            await asyncio.wait_for(fut, float(self.ack_timeout))
        except (TimeoutError, asyncio.TimeoutError):
            # Withdraw the abandoned future so a future ack doesn't
            # resolve it instead of the frame it belongs to.
            with contextlib.suppress(ValueError):
                self._pending_acks.remove(fut)
            raise TimeoutError(
                f"frame was not acknowledged within {self.ack_timeout}s — "
                "the client may have disconnected"
            ) from None

    async def _send_frame(self, packet: bytes) -> None:
        self._last_packet = packet
        await self._send_and_wait(packet)

    def _local_data_transport(self) -> bool:
        try:
            page = self.page
        except RuntimeError:  # not added to a page yet
            return False
        return bool(getattr(page.session.connection, "local_data_transport", False))

    # -- public API ---------------------------------------------------------

    async def render(self, image: Any, *, premultiplied: bool = False) -> None:
        """
        Display a Pillow image or a NumPy-style array and wait until the
        client has shown it.

        Args:
            image: A `PIL.Image.Image` (any mode; converted to RGBA as
                needed), or an object exposing `__array_interface__`
                (e.g. a NumPy array) of shape `(height, width, 4)` or
                `(height, width, 3)` with `uint8` values.
            premultiplied: Set to `True` if RGB values are already
                premultiplied by alpha to skip the premultiplication step.

        Raises:
            TypeError: If `image` is neither a Pillow image nor an
                array-like object.
            TimeoutError: If the client widget doesn't attach within
                :attr:`ready_timeout`.
        """
        if hasattr(image, "mode") and hasattr(image, "tobytes"):
            await self._render_pil(image, premultiplied)
        elif hasattr(image, "__array_interface__"):
            await self._render_array(image, premultiplied)
        else:
            raise TypeError(
                "RawImage.render() accepts a PIL.Image.Image or an object "
                f"with __array_interface__, got {type(image).__name__}"
            )

    async def render_rgba(
        self,
        width: int,
        height: int,
        pixels: bytes,
        *,
        premultiplied: bool = True,
    ) -> None:
        """
        Display a raw RGBA8888 frame and wait until the client has shown it.

        Args:
            width: Frame width in physical pixels.
            height: Frame height in physical pixels.
            pixels: Tightly packed RGBA8888 bytes, `width * height * 4`
                long. RGB values must be premultiplied by alpha (fully
                opaque frames are premultiplied by definition).
            premultiplied: Set to `False` if RGB values are straight
                (non-premultiplied); Pillow is then required to
                premultiply them.

        Raises:
            ValueError: If `pixels` has the wrong length.
            TimeoutError: If the client widget doesn't attach within
                :attr:`ready_timeout`.
        """
        if len(pixels) != width * height * 4:
            raise ValueError(
                f"pixels must be width * height * 4 = {width * height * 4} "
                f"bytes, got {len(pixels)}"
            )
        if not premultiplied and _rgba_is_opaque(pixels):
            premultiplied = True  # straight == premultiplied when opaque
        local = self._local_data_transport()
        if not premultiplied:
            # Straight alpha: Pillow is required either to premultiply
            # (local raw upload) or to PNG-encode (remote).
            img = _pil_from_rgba(width, height, pixels)
            if local:
                pixels = _premultiply_pil(img).tobytes()
            else:
                await self._send_frame(
                    b"\x01" + await asyncio.to_thread(_pil_to_png_bytes, img)
                )
                return
        elif not local and _rgba_is_opaque(pixels):
            # Opaque frames PNG-encode losslessly (nothing to premultiply);
            # non-opaque premultiplied frames have no straight-alpha source
            # to encode and are sent raw.
            img = _try_pil_from_rgba(width, height, pixels)
            if img is not None:
                await self._send_frame(
                    b"\x01" + await asyncio.to_thread(_pil_to_png_bytes, img)
                )
                return
        await self._send_frame(_encode_raw_packet(width, height, pixels))

    async def render_encoded(self, data: bytes) -> None:
        """
        Display an encoded image (PNG, JPEG, WebP, ...) and wait until the
        client has shown it.

        The bytes still travel over the data channel (skipping the Flet
        protocol), but the client decodes them with its image codecs
        instead of a raw pixel upload.

        Args:
            data: Encoded image bytes.

        Raises:
            TimeoutError: If the client widget doesn't attach within
                :attr:`ready_timeout`.
        """
        await self._send_frame(b"\x01" + data)

    async def clear(self) -> None:
        """
        Clear the displayed frame.
        """
        self._last_packet = None
        await self._send_and_wait(b"\x03")

    # -- input paths ----------------------------------------------------------

    async def _render_pil(self, image: Any, premultiplied: bool) -> None:
        if not self._local_data_transport():
            # PNG carries straight alpha — encode the original image,
            # never a premultiplied copy. Encoding is CPU-heavy; keep it
            # off the event loop.
            await self._send_frame(
                b"\x01" + await asyncio.to_thread(_pil_to_png_bytes, image)
            )
            return
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        if not premultiplied:
            image = _premultiply_pil(image)
        width, height = image.size
        await self._send_frame(_encode_raw_packet(width, height, image.tobytes()))

    async def _render_array(self, array: Any, premultiplied: bool) -> None:
        # An object with __array_interface__ guarantees numpy is importable
        # in practice; import lazily so flet itself never depends on it.
        import numpy as np

        arr = np.asarray(array)
        if arr.dtype != np.uint8 or arr.ndim != 3 or arr.shape[2] not in (3, 4):
            raise TypeError(
                "array must be uint8 with shape (height, width, 4) or "
                f"(height, width, 3), got {arr.dtype} {arr.shape}"
            )
        if arr.shape[2] == 3:
            rgba = np.empty(arr.shape[:2] + (4,), dtype=np.uint8)
            rgba[:, :, :3] = arr
            rgba[:, :, 3] = 255
            arr = rgba
            premultiplied = True  # opaque
        if not self._local_data_transport():
            try:
                from PIL import Image as PILImage
            except ImportError:
                pass
            else:
                if premultiplied and (arr[:, :, 3] != 255).any():
                    # No straight-alpha source to encode — send raw.
                    await self._send_frame(self._array_packet(np, arr, True))
                    return
                img = PILImage.frombuffer(
                    "RGBA",
                    (arr.shape[1], arr.shape[0]),
                    np.ascontiguousarray(arr).tobytes(),
                )
                await self._send_frame(
                    b"\x01" + await asyncio.to_thread(_pil_to_png_bytes, img)
                )
                return
        await self._send_frame(self._array_packet(np, arr, premultiplied))

    @staticmethod
    def _array_packet(np: Any, arr: Any, premultiplied: bool) -> bytes:
        if not premultiplied and (arr[:, :, 3] != 255).any():
            # Flutter's rgba8888 upload assumes premultiplied alpha.
            out = arr.copy()
            a = out[:, :, 3:4].astype(np.uint16)
            out[:, :, :3] = (out[:, :, :3].astype(np.uint16) * a // 255).astype(
                np.uint8
            )
            arr = out
        arr = np.ascontiguousarray(arr)
        return _encode_raw_packet(arr.shape[1], arr.shape[0], arr.tobytes())


# -- Pillow helpers (Pillow is an optional dependency; import lazily) ---------


def _premultiply_pil(image: Any) -> Any:
    """
    Premultiplies RGB by alpha in an RGBA Pillow image.

    Flutter's rgba8888 texture upload assumes premultiplied alpha, while
    Pillow produces straight alpha. All per-pixel work happens in Pillow's
    C loops: an opaque image is detected with `getextrema()` and returned
    as-is; otherwise each color band is multiplied by the alpha band.
    """
    alpha = image.getchannel("A")
    if alpha.getextrema() == (255, 255):
        return image
    from PIL import Image as PILImage
    from PIL import ImageChops

    r, g, b, a = image.split()
    return PILImage.merge(
        "RGBA",
        (
            ImageChops.multiply(r, a),
            ImageChops.multiply(g, a),
            ImageChops.multiply(b, a),
            a,
        ),
    )


def _pil_from_rgba(width: int, height: int, pixels: bytes) -> Any:
    try:
        from PIL import Image as PILImage
    except ImportError:
        raise RuntimeError(
            "Pillow is required to premultiply raw RGBA pixels; install it "
            "or pass premultiplied pixels"
        ) from None
    return PILImage.frombuffer("RGBA", (width, height), pixels)


def _try_pil_from_rgba(width: int, height: int, pixels: bytes) -> Optional[Any]:
    try:
        from PIL import Image as PILImage
    except ImportError:
        return None
    return PILImage.frombuffer("RGBA", (width, height), pixels)


def _rgba_is_opaque(pixels: bytes) -> bool:
    """
    Whether every alpha byte in tightly packed RGBA8888 is 255.

    The strided slice and count both run in C — no per-pixel Python loop.
    """
    alphas = pixels[3::4]
    return alphas.count(255) == len(alphas)


def _pil_to_png_bytes(image: Any) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _encode_raw_packet(width: int, height: int, rgba: bytes) -> bytes:
    """
    Encodes a raw full frame into a 0x04 wire packet:
    `[0x04][width u32 LE][height u32 LE][premultiplied RGBA8888]`.
    """
    pkt = bytearray(9 + len(rgba))
    pkt[0] = 0x04
    pkt[1:5] = width.to_bytes(4, "little")
    pkt[5:9] = height.to_bytes(4, "little")
    pkt[9:] = rgba
    return bytes(pkt)
