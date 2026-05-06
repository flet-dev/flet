import flet as ft
import flet_video as ftv

SAMPLE_VTT = """WEBVTT

00:00:00.000 --> 00:00:04.000
Welcome to flet-video!

00:00:04.000 --> 00:00:08.000
Subtitles are styled via VideoSubtitleConfiguration.

00:00:08.000 --> 00:00:14.000
This track is provided as raw VTT text.
"""


def main(page: ft.Page):
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    subtitle_track = ftv.VideoSubtitleTrack(
        src=SAMPLE_VTT,
        title="English",
        language="en",
    )

    def handle_change(e: ft.Event[ft.Switch]):
        if e.control.value:
            video.subtitle_track = subtitle_track
        else:
            video.subtitle_track = ftv.VideoSubtitleTrack.none()

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    video := ftv.Video(
                        expand=True,
                        autoplay=False,
                        playlist=[
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                            ),
                        ],
                        subtitle_track=subtitle_track,
                        subtitle_configuration=ftv.VideoSubtitleConfiguration(
                            text_align=ft.TextAlign.CENTER,
                            text_style=ft.TextStyle(
                                size=24,
                                color=ft.Colors.YELLOW,
                                weight=ft.FontWeight.BOLD,
                                bgcolor=ft.Colors.BLACK_54,
                            ),
                        ),
                    ),
                    ft.Switch(
                        value=True, label="Show Subtitles", on_change=handle_change
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
