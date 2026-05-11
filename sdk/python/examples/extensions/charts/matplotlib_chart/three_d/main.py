import logging

import matplotlib.pyplot as plt

import flet as ft
import flet_charts

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    from mpl_toolkits.mplot3d import axes3d

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    X, Y, Z = axes3d.get_test_data(0.1)

    # Plot the 3D surface
    ax.plot_surface(
        X, Y, Z, edgecolor="royalblue", lw=0.5, rstride=8, cstride=8, alpha=0.3
    )

    # Plot projections of the contours for each dimension.  By choosing offsets
    # that match the appropriate axes limits, the projected contours will sit on
    # the 'walls' of the graph
    ax.contourf(X, Y, Z, zdir="z", offset=-100, cmap="coolwarm")
    ax.contourf(X, Y, Z, zdir="x", offset=-40, cmap="coolwarm")
    ax.contourf(X, Y, Z, zdir="y", offset=40, cmap="coolwarm")

    ax.set(
        xlim=(-40, 40),
        ylim=(-40, 40),
        zlim=(-100, 100),
        xlabel="X",
        ylabel="Y",
        zlabel="Z",
    )

    page.add(
        ft.SafeArea(
            content=flet_charts.MatplotlibChartWithToolbar(figure=fig, expand=True),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
