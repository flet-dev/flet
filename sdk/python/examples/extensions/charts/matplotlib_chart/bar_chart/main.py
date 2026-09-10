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

import flet as ft
import flet_charts as fch


def main(page: ft.Page):
    fig, ax = plt.subplots()

    fruits = ["apple", "blueberry", "cherry", "orange"]
    counts = [40, 100, 30, 55]
    bar_labels = ["red", "blue", "_red", "orange"]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel("fruit supply")
    ax.set_title("Fruit supply by kind and color")
    ax.legend(title="Fruit color")

    page.add(
        ft.SafeArea(
            expand=True,
            content=fch.MatplotlibChart(figure=fig, expand=True),
        )
    )


if __name__ == "__main__":
    ft.run(main)
