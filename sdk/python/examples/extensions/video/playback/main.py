import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    async def handle_play(e: ft.Event[ft.Button]):
        await video.play()

    async def handle_play_or_pause(e: ft.Event[ft.Button]):
        await video.play_or_pause()

    async def handle_pause(e: ft.Event[ft.Button]):
        await video.pause()

    async def handle_stop(e: ft.Event[ft.Button]):
        await video.stop()

    async def handle_seek(e: ft.Event[ft.Button]):
        await video.seek(ft.Duration(seconds=10))

    async def handle_next(e: ft.Event[ft.Button]):
        await video.next()

    async def handle_previous(e: ft.Event[ft.Button]):
        await video.previous()

    async def handle_status(e: ft.Event[ft.Button]):
        playing = await video.is_playing()
        position = (await video.get_current_position()).in_seconds
        duration = (await video.get_duration()).in_seconds
        page.show_dialog(
            ft.SnackBar(
                f"Playing?: {playing} | Duration: {duration}s | Position: {position}s"
            )
        )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    video := ftv.Video(
                        expand=True,
                        playlist=[
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                            ),
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
                            ),
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Button("Play", on_click=handle_play),
                            ft.Button("Play Or Pause", on_click=handle_play_or_pause),
                            ft.Button("Pause", on_click=handle_pause),
                            ft.Button("Stop", on_click=handle_stop),
                            ft.Button("Seek 10s", on_click=handle_seek),
                            ft.Button("Previous", on_click=handle_previous),
                            ft.Button("Next", on_click=handle_next),
                            ft.Button("Show Status", on_click=handle_status),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
