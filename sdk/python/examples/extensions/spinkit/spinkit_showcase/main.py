import flet_spinkit as fsk

import flet as ft

SPINNERS = [
    ("RotatingPlain", fsk.SpinKitRotatingPlain),
    ("DoubleBounce", fsk.SpinKitDoubleBounce),
    ("Wave", fsk.SpinKitWave),
    ("WanderingCubes", fsk.SpinKitWanderingCubes),
    ("FadingFour", fsk.SpinKitFadingFour),
    ("FadingCube", fsk.SpinKitFadingCube),
    ("Pulse", fsk.SpinKitPulse),
    ("ChasingDots", fsk.SpinKitChasingDots),
    ("ThreeBounce", fsk.SpinKitThreeBounce),
    ("Circle", fsk.SpinKitCircle),
    ("CubeGrid", fsk.SpinKitCubeGrid),
    ("FadingCircle", fsk.SpinKitFadingCircle),
    ("RotatingCircle", fsk.SpinKitRotatingCircle),
    ("FoldingCube", fsk.SpinKitFoldingCube),
    ("PumpingHeart", fsk.SpinKitPumpingHeart),
    ("HourGlass", fsk.SpinKitHourGlass),
    ("PouringHourGlass", fsk.SpinKitPouringHourGlass),
    ("PouringHourGlassRefined", fsk.SpinKitPouringHourGlassRefined),
    ("FadingGrid", fsk.SpinKitFadingGrid),
    ("Ring", fsk.SpinKitRing),
    ("Ripple", fsk.SpinKitRipple),
    ("DualRing", fsk.SpinKitDualRing),
    ("SpinningCircle", fsk.SpinKitSpinningCircle),
    ("SpinningLines", fsk.SpinKitSpinningLines),
    ("SquareCircle", fsk.SpinKitSquareCircle),
    ("ThreeInOut", fsk.SpinKitThreeInOut),
    ("DancingSquare", fsk.SpinKitDancingSquare),
    ("PianoWave", fsk.SpinKitPianoWave),
    ("PulsingGrid", fsk.SpinKitPulsingGrid),
    ("PumpCurve", fsk.SpinKitPumpCurve),
    ("RingCurve", fsk.SpinKitRingCurve),
]

COLORS = {
    "Blue": ft.Colors.BLUE,
    "Red": ft.Colors.RED,
    "Green": ft.Colors.GREEN,
    "Purple": ft.Colors.PURPLE,
    "Orange": ft.Colors.ORANGE,
    "Teal": ft.Colors.TEAL,
}


def main(page: ft.Page):
    page.title = "SpinKit Showcase"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    selected_color = ft.Colors.BLUE
    spinner_size = 48.0

    grid = ft.GridView(
        expand=False,
        runs_count=3,
        max_extent=180,
        child_aspect_ratio=0.9,
        spacing=12,
        run_spacing=12,
    )

    def make_spinner(cls):
        kwargs = {"color": selected_color, "size": spinner_size}
        if cls is fsk.SpinKitWave:
            kwargs["wave_type"] = fsk.SpinKitWaveType.CENTER
        elif cls in (fsk.SpinKitRing, fsk.SpinKitDualRing, fsk.SpinKitRingCurve):
            kwargs["line_width"] = 5.0
        elif cls is fsk.SpinKitRipple:
            kwargs["border_width"] = 4.0
        elif cls is fsk.SpinKitSpinningLines:
            kwargs["line_width"] = 2.0
        return cls(**kwargs)

    def rebuild():
        grid.controls.clear()
        for name, cls in SPINNERS:
            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=make_spinner(cls),
                                alignment=ft.Alignment.CENTER,
                                expand=True,
                            ),
                            ft.Text(
                                name,
                                size=11,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    border=ft.border.all(
                        1, ft.Colors.with_opacity(0.12, ft.Colors.ON_SURFACE)
                    ),
                    border_radius=12,
                    padding=12,
                )
            )
        page.update()

    def on_color_change(e):
        nonlocal selected_color
        selected_color = COLORS[e.control.selected.pop()]
        e.control.selected = {[k for k, v in COLORS.items() if v == selected_color][0]}
        e.control.update()
        rebuild()

    def on_size_change(e):
        nonlocal spinner_size
        spinner_size = e.control.value
        size_label.value = f"Size: {int(spinner_size)}px"
        size_label.update()
        rebuild()

    color_selector = ft.SegmentedButton(
        segments=[ft.Segment(value=name, label=ft.Text(name)) for name in COLORS],
        selected={"Blue"},
        on_change=on_color_change,
        allow_empty_selection=False,
        allow_multiple_selection=False,
    )

    size_label = ft.Text(f"Size: {int(spinner_size)}px")
    size_slider = ft.Slider(
        min=24,
        max=80,
        value=spinner_size,
        divisions=14,
        on_change_end=on_size_change,
        expand=True,
    )

    rebuild()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Text("SpinKit Showcase", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"{len(SPINNERS)} spinner animations from flutter_spinkit",
                        size=13,
                    ),
                    ft.Divider(),
                    ft.Text("Color", weight=ft.FontWeight.W_500),
                    color_selector,
                    ft.Row([size_label, size_slider]),
                    ft.Divider(),
                    grid,
                ],
                spacing=12,
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
