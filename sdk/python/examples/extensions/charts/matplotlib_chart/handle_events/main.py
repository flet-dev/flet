import os
import sys

# Load Matplotlib's `ft2font` extension with RTLD_DEEPBIND, so it binds to the
# FreeType and harfbuzz it was built against.
#
# A packaged Linux app embeds Python in the Flutter process, where GTK has
# already loaded the system libfreetype/libharfbuzz into the global symbol
# namespace. `ft2font` statically links its own copies but also exports their
# symbols, so its internal calls resolve to the system ones instead. The ABI
# mismatch corrupts glyph metrics - a 10pt "-40" measures millions of points
# wide - and every text draw then fails with
# "FT_Render_Glyph ... error 0x62: raster overflow".
#
# Must run before Matplotlib is imported: the extension is cached after its
# first load. No-op wherever the flag is absent (macOS, Windows, Android, iOS,
# Pyodide) - none of those resolve symbols through a flat global namespace.
if hasattr(os, "RTLD_DEEPBIND"):
    _dlopenflags = sys.getdlopenflags()
    sys.setdlopenflags(_dlopenflags | os.RTLD_DEEPBIND)
    try:
        from matplotlib import ft2font  # noqa: F401
    finally:
        sys.setdlopenflags(_dlopenflags)


import matplotlib.pyplot as plt
import numpy as np

import flet as ft
import flet_charts as fch

state = {}


def main(page: ft.Page):
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    X = np.random.rand(100, 200)
    xs = np.mean(X, axis=1)
    ys = np.std(X, axis=1)

    fig, (ax, ax2) = plt.subplots(2, 1)
    ax.set_title("click on point to plot time series")
    (line,) = ax.plot(xs, ys, "o", picker=True, pickradius=5)

    class PointBrowser:
        """
        Click on a point to select and highlight it -- the data that
        generated the point will be shown in the lower Axes.  Use the 'n'
        and 'p' keys to browse through the next and previous points
        """

        def __init__(self):
            self.lastind = 0

            self.text = ax.text(
                0.05, 0.95, "selected: none", transform=ax.transAxes, va="top"
            )
            (self.selected,) = ax.plot(
                [xs[0]], [ys[0]], "o", ms=12, alpha=0.4, color="yellow", visible=False
            )

        def on_press(self, event):
            if self.lastind is None:
                return
            if event.key not in ("n", "p"):
                return
            inc = 1 if event.key == "n" else -1

            self.lastind += inc
            self.lastind = np.clip(self.lastind, 0, len(xs) - 1)
            self.update()

        def on_pick(self, event):
            if event.artist != line:
                return True

            N = len(event.ind)
            if not N:
                return True

            # the click locations
            x = event.mouseevent.xdata
            y = event.mouseevent.ydata

            distances = np.hypot(x - xs[event.ind], y - ys[event.ind])
            indmin = distances.argmin()
            dataind = event.ind[indmin]

            self.lastind = dataind
            self.update()

        def update(self):
            if self.lastind is None:
                return

            dataind = self.lastind

            ax2.clear()
            ax2.plot(X[dataind])

            ax2.text(
                0.05,
                0.9,
                f"mu={xs[dataind]:1.3f}\nsigma={ys[dataind]:1.3f}",
                transform=ax2.transAxes,
                va="top",
            )
            ax2.set_ylim(-0.5, 1.5)
            self.selected.set_visible(True)
            self.selected.set_data([xs[dataind]], [ys[dataind]])

            self.text.set_text(f"selected: {dataind:d}")
            fig.canvas.draw()

    browser = PointBrowser()
    state["browser"] = browser

    fig.canvas.mpl_connect("pick_event", browser.on_pick)
    fig.canvas.mpl_connect("key_press_event", browser.on_press)

    # plt.show()

    page.add(
        ft.SafeArea(
            expand=True,
            content=fch.MatplotlibChartWithToolbar(figure=fig, expand=True),
        )
    )


if __name__ == "__main__":
    ft.run(main)
