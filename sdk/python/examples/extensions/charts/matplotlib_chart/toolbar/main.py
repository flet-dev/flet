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


def main(page: ft.Page):
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))  # white noise 1
    nse2 = np.random.randn(len(t))  # white noise 2

    # Two signals with a coherent part at 10Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel("time")
    axs[0].set_ylabel("s1 and s2")
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1.0 / dt)
    axs[1].set_ylabel("coherence")

    fig.tight_layout()

    page.add(
        ft.SafeArea(
            expand=True,
            content=fch.MatplotlibChartWithToolbar(figure=fig, expand=True),
        )
    )


if __name__ == "__main__":
    ft.run(main)
