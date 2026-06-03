import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            expand=True,
            content=ftv.Video(
                expand=True,
                autoplay=True,
                playlist=[
                    ftv.VideoMedia(
                        "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
