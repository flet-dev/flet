import flet_spinkit as fsk

import flet as ft

SPINNERS = [
    ("RotatingPlain", fsk.RotatingPlain),
    ("DoubleBounce", fsk.DoubleBounce),
    ("Wave", fsk.Wave),
    ("WanderingCubes", fsk.WanderingCubes),
    ("FadingFour", fsk.FadingFour),
    ("FadingCube", fsk.FadingCube),
    ("Pulse", fsk.Pulse),
    ("ChasingDots", fsk.ChasingDots),
    ("ThreeBounce", fsk.ThreeBounce),
    ("Circle", fsk.Circle),
    ("CubeGrid", fsk.CubeGrid),
    ("FadingCircle", fsk.FadingCircle),
    ("RotatingCircle", fsk.RotatingCircle),
    ("FoldingCube", fsk.FoldingCube),
    ("PumpingHeart", fsk.PumpingHeart),
    ("HourGlass", fsk.HourGlass),
    ("PouringHourGlass", fsk.PouringHourGlass),
    ("PouringHourGlassRefined", fsk.PouringHourGlassRefined),
    ("FadingGrid", fsk.FadingGrid),
    ("Ring", fsk.Ring),
    ("Ripple", fsk.Ripple),
    ("DualRing", fsk.DualRing),
    ("SpinningCircle", fsk.SpinningCircle),
    ("SpinningLines", fsk.SpinningLines),
    ("SquareCircle", fsk.SquareCircle),
    ("ThreeInOut", fsk.ThreeInOut),
    ("DancingSquare", fsk.DancingSquare),
    ("PianoWave", fsk.PianoWave),
    ("PulsingGrid", fsk.PulsingGrid),
    ("WaveSpinner", fsk.WaveSpinner),
]


def main(page: ft.Page):
    page.title = "SpinKit Showcase"
    page.theme_mode = ft.ThemeMode.DARK
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
                                color=ft.Colors.WHITE70,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                    border_radius=12,
                    padding=12,
                )
                for name, cls in SPINNERS
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
