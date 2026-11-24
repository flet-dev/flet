import numpy as np
from matplotlib import _api
from matplotlib.backends import backend_webagg_core


class FigureCanvasFletAgg(backend_webagg_core.FigureCanvasWebAggCore):
    """Canvas implementation used to render Matplotlib figures in Flet."""

    manager_class = _api.classproperty(lambda cls: FigureManagerFletAgg)
    supports_blit = False

    def get_raw_frame(self):
        """Raw analogue of `get_diff_image()` for local transports.

        Returns `(width, height, rgba)` when the renderer holds newer pixels
        than the last sent frame, else `None`. Raw frames are always full
        frames — no diffing, no PNG encoding. Unless premultiplication made
        a copy, `rgba` aliases the live Agg buffer that the next draw
        mutates in place, so the caller must consume it synchronously.
        """
        if not self._png_is_old:
            return None
        renderer = self.get_renderer()
        buf = renderer.buffer_rgba()  # memoryview, straight alpha
        w, h = int(renderer.width), int(renderer.height)
        pixels = np.asarray(buf)
        if (pixels[:, :, 3] != 255).any():
            # Flutter's rgba8888 upload assumes premultiplied alpha; Agg
            # produces straight alpha. Premultiply only when needed.
            out = pixels.copy()
            a = out[:, :, 3:4].astype(np.uint16)
            out[:, :, :3] = (out[:, :, :3].astype(np.uint16) * a // 255).astype(
                np.uint8
            )
            buf = out.tobytes()
        # Raw mode deliberately leaves `_last_buff` untouched: if the PNG
        # path ever runs afterwards, the shape mismatch forces a full frame.
        self._force_full = False
        self._png_is_old = False
        return (w, h, buf)


class FigureManagerFletAgg(backend_webagg_core.FigureManagerWebAgg):
    """Figure manager binding Matplotlib WebAgg tooling to Flet transport."""

    _toolbar2_class = backend_webagg_core.NavigationToolbar2WebAgg

    def refresh_all(self):
        if not self.web_sockets:
            return
        raw = {s for s in self.web_sockets if getattr(s, "wants_raw_frames", False)}
        if raw and raw == self.web_sockets:
            frame = self.canvas.get_raw_frame()
            if frame is not None:
                for s in raw:
                    s.send_binary(frame)  # tuple => raw frame
        else:
            # All-PNG, or mixed transports (same figure shown on two
            # connection types — practically impossible in one process):
            # everyone gets the PNG full/diff path.
            super().refresh_all()


FigureCanvas = FigureCanvasFletAgg
FigureManager = FigureManagerFletAgg
interactive = True
