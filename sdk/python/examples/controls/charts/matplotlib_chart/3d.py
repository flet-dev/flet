import logging

import flet_charts
import matplotlib.pyplot as plt
import numpy as np

import flet as ft

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    plt.style.use("_mpl-gallery")

    # Make data for a double helix
    n = 50
    theta = np.linspace(0, 2 * np.pi, n)
    x1 = np.cos(theta)
    y1 = np.sin(theta)
    z1 = np.linspace(0, 1, n)
    x2 = np.cos(theta + np.pi)
    y2 = np.sin(theta + np.pi)
    z2 = z1

    # Plot with defined figure size
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8, 6))
    ax.fill_between(x1, y1, z1, x2, y2, z2, alpha=0.5)
    ax.plot(x1, y1, z1, linewidth=2, color="C0")
    ax.plot(x2, y2, z2, linewidth=2, color="C0")

    ax.set(xticklabels=[], yticklabels=[], zticklabels=[])

    page.add(flet_charts.MatplotlibChartWithToolbar(figure=fig))


ft.run(main)
