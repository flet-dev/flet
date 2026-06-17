import flet_spinkit as fsk

import flet as ft


def section(title: str, controls: list) -> ft.Column:
    return ft.Column(
        [
            ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
            ft.Row(controls, spacing=24, wrap=True),
        ],
        spacing=12,
    )


def labeled(spinner, label: str) -> ft.Column:
    return ft.Column(
        [
            ft.Container(
                content=spinner,
                alignment=ft.Alignment.CENTER,
                width=80,
                height=80,
            ),
            ft.Text(
                label,
                size=10,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )


def main(page: ft.Page):
    page.title = "SpinKit Properties"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 24

    page.add(
        ft.Text("SpinKit Properties", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
        # Colors
        section(
            "color",
            [
                labeled(fsk.RotatingCircle(color=ft.Colors.BLUE, size=50), "BLUE"),
                labeled(fsk.RotatingCircle(color=ft.Colors.RED, size=50), "RED"),
                labeled(fsk.RotatingCircle(color=ft.Colors.GREEN, size=50), "GREEN"),
                labeled(fsk.RotatingCircle(color=ft.Colors.ORANGE, size=50), "ORANGE"),
                labeled(fsk.RotatingCircle(color=ft.Colors.PURPLE, size=50), "PURPLE"),
                labeled(fsk.RotatingCircle(color=ft.Colors.TEAL, size=50), "TEAL"),
            ],
        ),
        ft.Divider(height=8),
        # Sizes
        section(
            "size",
            [
                labeled(fsk.ThreeBounce(color=ft.Colors.BLUE, size=20), "20"),
                labeled(fsk.ThreeBounce(color=ft.Colors.BLUE, size=30), "30"),
                labeled(fsk.ThreeBounce(color=ft.Colors.BLUE, size=40), "40"),
                labeled(fsk.ThreeBounce(color=ft.Colors.BLUE, size=50), "50"),
                labeled(fsk.ThreeBounce(color=ft.Colors.BLUE, size=70), "70"),
            ],
        ),
        ft.Divider(height=8),
        # Durations
        section(
            "duration",
            [
                labeled(
                    fsk.Pulse(
                        color=ft.Colors.BLUE,
                        size=50,
                        duration=ft.Duration(milliseconds=400),
                    ),
                    "400ms",
                ),
                labeled(
                    fsk.Pulse(
                        color=ft.Colors.BLUE,
                        size=50,
                        duration=ft.Duration(milliseconds=700),
                    ),
                    "700ms",
                ),
                labeled(
                    fsk.Pulse(
                        color=ft.Colors.BLUE,
                        size=50,
                        duration=ft.Duration(milliseconds=1000),
                    ),
                    "1000ms",
                ),
                labeled(
                    fsk.Pulse(
                        color=ft.Colors.BLUE,
                        size=50,
                        duration=ft.Duration(milliseconds=2000),
                    ),
                    "2000ms",
                ),
                labeled(
                    fsk.Pulse(
                        color=ft.Colors.BLUE,
                        size=50,
                        duration=ft.Duration(milliseconds=4000),
                    ),
                    "4000ms",
                ),
            ],
        ),
        ft.Divider(height=8),
        # Wave — wave_type
        section(
            "Wave · wave_type",
            [
                labeled(
                    fsk.Wave(
                        color=ft.Colors.BLUE, size=50, wave_type=fsk.WaveType.START
                    ),
                    "START",
                ),
                labeled(
                    fsk.Wave(
                        color=ft.Colors.BLUE, size=50, wave_type=fsk.WaveType.CENTER
                    ),
                    "CENTER",
                ),
                labeled(
                    fsk.Wave(color=ft.Colors.BLUE, size=50, wave_type=fsk.WaveType.END),
                    "END",
                ),
            ],
        ),
        ft.Divider(height=8),
        # Wave — item_count
        section(
            "Wave · item_count",
            [
                labeled(fsk.Wave(color=ft.Colors.BLUE, size=50, item_count=3), "3"),
                labeled(fsk.Wave(color=ft.Colors.BLUE, size=50, item_count=5), "5"),
                labeled(fsk.Wave(color=ft.Colors.BLUE, size=50, item_count=7), "7"),
                labeled(fsk.Wave(color=ft.Colors.BLUE, size=50, item_count=10), "10"),
            ],
        ),
        ft.Divider(height=8),
        # Ring — line_width
        section(
            "Ring · line_width",
            [
                labeled(fsk.Ring(color=ft.Colors.BLUE, size=50, line_width=2), "2"),
                labeled(fsk.Ring(color=ft.Colors.BLUE, size=50, line_width=5), "5"),
                labeled(fsk.Ring(color=ft.Colors.BLUE, size=50, line_width=8), "8"),
                labeled(fsk.Ring(color=ft.Colors.BLUE, size=50, line_width=12), "12"),
            ],
        ),
        ft.Divider(height=8),
        # DualRing — line_width
        section(
            "DualRing · line_width",
            [
                labeled(fsk.DualRing(color=ft.Colors.BLUE, size=50, line_width=2), "2"),
                labeled(fsk.DualRing(color=ft.Colors.BLUE, size=50, line_width=5), "5"),
                labeled(fsk.DualRing(color=ft.Colors.BLUE, size=50, line_width=8), "8"),
                labeled(
                    fsk.DualRing(color=ft.Colors.BLUE, size=50, line_width=12), "12"
                ),
            ],
        ),
        ft.Divider(height=8),
        # Ripple — border_width
        section(
            "Ripple · border_width",
            [
                labeled(fsk.Ripple(color=ft.Colors.BLUE, size=50, border_width=2), "2"),
                labeled(fsk.Ripple(color=ft.Colors.BLUE, size=50, border_width=4), "4"),
                labeled(fsk.Ripple(color=ft.Colors.BLUE, size=50, border_width=8), "8"),
                labeled(
                    fsk.Ripple(color=ft.Colors.BLUE, size=50, border_width=14), "14"
                ),
            ],
        ),
        ft.Divider(height=8),
        # SpinningLines — line_width
        section(
            "SpinningLines · line_width",
            [
                labeled(
                    fsk.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=1), "1"
                ),
                labeled(
                    fsk.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=2), "2"
                ),
                labeled(
                    fsk.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=4), "4"
                ),
                labeled(
                    fsk.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=6), "6"
                ),
            ],
        ),
        ft.Divider(height=8),
        # PianoWave — item_count
        section(
            "PianoWave · item_count",
            [
                labeled(
                    fsk.PianoWave(color=ft.Colors.BLUE, size=50, item_count=3), "3"
                ),
                labeled(
                    fsk.PianoWave(color=ft.Colors.BLUE, size=50, item_count=5), "5"
                ),
                labeled(
                    fsk.PianoWave(color=ft.Colors.BLUE, size=50, item_count=8), "8"
                ),
                labeled(
                    fsk.PianoWave(color=ft.Colors.BLUE, size=50, item_count=12), "12"
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
