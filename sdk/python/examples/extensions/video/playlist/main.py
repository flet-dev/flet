import random

import flet as ft
import flet_video as ftv

media = [
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4"
    ),
]


def main(page: ft.Page):
    def handle_add(e: ft.Event[ft.Button]):
        video.playlist.append(random.choice(media))

    def handle_remove(e: ft.Event[ft.Button]):
        if video.playlist:
            video.playlist.pop(random.randint(0, len(video.playlist) - 1))

    def handle_replace(e: ft.Event[ft.Button]):
        video.playlist = random.sample(media, 3)

    async def handle_next(e: ft.Event[ft.Button]):
        await video.next()

    async def handle_previous(e: ft.Event[ft.Button]):
        await video.previous()

    async def handle_jump(e: ft.Event[ft.Button]):
        await video.jump_to(0)

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    video := ftv.Video(
                        expand=True,
                        autoplay=True,
                        playlist=media[:2],
                        playlist_mode=ftv.PlaylistMode.LOOP,
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Button("Add Random", on_click=handle_add),
                            ft.Button("Remove Random", on_click=handle_remove),
                            ft.Button("Replace Playlist", on_click=handle_replace),
                            ft.Button("Next", on_click=handle_next),
                            ft.Button("Previous", on_click=handle_previous),
                            ft.Button("Jump to First", on_click=handle_jump),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
