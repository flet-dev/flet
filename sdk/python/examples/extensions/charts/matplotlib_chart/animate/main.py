import logging
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
import flet_charts

logging.basicConfig(level=logging.INFO)

state = {}


def main(page: ft.Page):
    import matplotlib.animation as animation

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    def random_walk(num_steps, max_step=0.05):
        """Return a 3D random walk as (num_steps, 3) array."""
        start_pos = np.random.random(3)
        steps = np.random.uniform(-max_step, max_step, size=(num_steps, 3))
        walk = start_pos + np.cumsum(steps, axis=0)
        return walk

    def update_lines(num, walks, lines):
        for line, walk in zip(lines, walks):
            line.set_data_3d(walk[:num, :].T)
        return lines

    # Data: 40 random walks as (num_steps, 3) arrays
    num_steps = 30
    walks = [random_walk(num_steps) for index in range(40)]

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Create lines initially without data
    lines = [ax.plot([], [], [])[0] for _ in walks]

    # Setting the Axes properties
    ax.set(xlim3d=(0, 1), xlabel="X")
    ax.set(ylim3d=(0, 1), ylabel="Y")
    ax.set(zlim3d=(0, 1), zlabel="Z")

    # Creating the Animation object
    state["anim"] = animation.FuncAnimation(
        fig, update_lines, num_steps, fargs=(walks, lines), interval=100
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=flet_charts.MatplotlibChartWithToolbar(figure=fig, expand=True),
        )
    )


if __name__ == "__main__":
    ft.run(main)
