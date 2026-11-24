import flet_spinkit as spins

import flet as ft

SPINNERS = [
    ("RotatingPlain", spins.RotatingPlain),
    ("DoubleBounce", spins.DoubleBounce),
    ("Wave", spins.Wave),
    ("WanderingCubes", spins.WanderingCubes),
    ("FadingFour", spins.FadingFour),
    ("FadingCube", spins.FadingCube),
    ("Pulse", spins.Pulse),
    ("ChasingDots", spins.ChasingDots),
    ("ThreeBounce", spins.ThreeBounce),
    ("Circle", spins.Circle),
    ("CubeGrid", spins.CubeGrid),
    ("FadingCircle", spins.FadingCircle),
    ("RotatingCircle", spins.RotatingCircle),
    ("FoldingCube", spins.FoldingCube),
    ("PumpingHeart", spins.PumpingHeart),
    ("HourGlass", spins.HourGlass),
    ("PouringHourGlass", spins.PouringHourGlass),
    ("PouringHourGlassRefined", spins.PouringHourGlassRefined),
    ("FadingGrid", spins.FadingGrid),
    ("Ring", spins.Ring),
    ("Ripple", spins.Ripple),
    ("DualRing", spins.DualRing),
    ("SpinningCircle", spins.SpinningCircle),
    ("SpinningLines", spins.SpinningLines),
    ("SquareCircle", spins.SquareCircle),
    ("ThreeInOut", spins.ThreeInOut),
    ("DancingSquare", spins.DancingSquare),
    ("PianoWave", spins.PianoWave),
    ("PulsingGrid", spins.PulsingGrid),
    ("WaveSpinner", spins.WaveSpinner),
]


def main(page: ft.Page):
    page.title = "SpinKit Showcase"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    color = ft.Colors.BLUE

    page.add(
        ft.GridView(
            runs_count=4,
            max_extent=160,
            child_aspect_ratio=0.9,
            spacing=12,
            run_spacing=12,
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=cls(color=color, size=50),
                                alignment=ft.Alignment.CENTER,
                                expand=True,
                            ),
                            ft.Text(
                                name,
                                size=11,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border_radius=12,
                    padding=12,
                )
                for name, cls in SPINNERS
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
