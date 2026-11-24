import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    label_style = ft.TextStyle(
        size=12,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ftv.Video(
                expand=True,
                playlist=[
                    ftv.VideoMedia("video-sample.mp4"),
                ],
                controls=ftv.MaterialDesktopVideoControls(
                    visible_on_mount=True,
                    primary_button_bar=[
                        ftv.VideoSkipPreviousButton(icon_color=ft.Colors.CYAN),
                        ftv.VideoPlayOrPauseButton(
                            icon_size=40,
                            icon_color=ft.Colors.CYAN,
                        ),
                        ftv.VideoSkipNextButton(
                            icon=ft.Icon(ft.Icons.FAST_FORWARD),
                            icon_color=ft.Colors.CYAN,
                        ),
                    ],
                    top_button_bar=[
                        ft.Text("Top button bar", style=label_style),
                        ftv.VideoSpacer(),
                        ftv.VideoFullscreenButton(icon_color=ft.Colors.AMBER),
                    ],
                    bottom_button_bar=[
                        ft.Text("Bottom button bar", style=label_style),
                        ftv.VideoSpacer(),
                        ftv.VideoPositionIndicator(
                            text_style=ft.TextStyle(
                                size=13,
                                color=ft.Colors.WHITE,
                            )
                        ),
                        ftv.VideoVolumeButton(
                            slider_width=96,
                            icon_color=ft.Colors.AMBER,
                        ),
                    ],
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
