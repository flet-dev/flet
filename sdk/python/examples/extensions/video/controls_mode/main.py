import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            expand=True,
            content=ftv.Video(
                expand=True,
                playlist=[
                    ftv.VideoMedia(
                        "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                    ),
                ],
                controls={
                    ftv.VideoControlsMode.NORMAL: ftv.MaterialDesktopVideoControls(
                        visible_on_mount=True,
                        bottom_button_bar=[
                            ftv.VideoPlayOrPauseButton(),
                            ftv.VideoSpacer(),
                            ft.Text("NORMAL Mode", weight=ft.FontWeight.BOLD),
                            ftv.VideoFullscreenButton(),
                        ],
                    ),
                    ftv.VideoControlsMode.FULLSCREEN: ftv.MaterialDesktopVideoControls(
                        visible_on_mount=True,
                        bottom_button_bar=[
                            ftv.VideoFullscreenButton(),
                            ftv.VideoSpacer(),
                            ft.Text("FULLSCREEN Mode", weight=ft.FontWeight.BOLD),
                            ftv.VideoPlayOrPauseButton(),
                        ],
                    ),
                },
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
