import random

import flet as ft
import flet_video as ftv

sample_media = [
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
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373709-603a7a89-2105-4e1b-a5a5-a6c3567c9a59.mp4",
        extras={
            "artist": "Thousand Foot Krutch",
            "album": "The End Is Where We Begin",
        },
        http_headers={
            "Foo": "Bar",
            "Accept": "*/*",
        },
    ),
]


def main(page: ft.Page):
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    async def handle_pause(e: ft.Event[ft.Button]):
        await video.pause()

    async def handle_play_or_pause(e: ft.Event[ft.Button]):
        await video.play_or_pause()

    async def handle_play(e: ft.Event[ft.Button]):
        await video.play()

    async def handle_stop(e: ft.Event[ft.Button]):
        await video.stop()

    async def handle_next(e: ft.Event[ft.Button]):
        await video.next()

    async def handle_previous(e: ft.Event[ft.Button]):
        await video.previous()

    def handle_volume_change(e: ft.Event[ft.Slider]):
        video.volume = e.control.value

    def handle_playback_rate_change(e: ft.Event[ft.Slider]):
        video.playback_rate = e.control.value

    async def handle_seek(e: ft.Event[ft.Button]):
        await video.seek(10000)

    async def handle_add_media(e: ft.Event[ft.Button]):
        await video.playlist_add(random.choice(sample_media))

    async def handle_remove_media(e: ft.Event[ft.Button]):
        r = random.randint(0, len(video.playlist) - 1)
        await video.playlist_remove(r)

    async def handle_jump(e: ft.Event[ft.Button]):
        await video.jump_to(0)

    async def handle_fullscreen(e: ft.Event[ft.Button]):
        video.fullscreen = True

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    video := ftv.Video(
                        expand=True,
                        playlist=sample_media[0:2],
                        playlist_mode=ftv.PlaylistMode.LOOP,
                        fill_color=ft.Colors.BLUE_400,
                        aspect_ratio=16 / 9,
                        volume=100,
                        autoplay=False,
                        filter_quality=ft.FilterQuality.HIGH,
                        muted=False,
                        on_load=lambda e: print("Video loaded successfully!"),
                        on_enter_fullscreen=lambda e: print("Entered fullscreen!"),
                        on_exit_fullscreen=lambda e: print("Exited fullscreen!"),
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Button("Play", on_click=handle_play),
                            ft.Button("Pause", on_click=handle_pause),
                            ft.Button("Play Or Pause", on_click=handle_play_or_pause),
                            ft.Button("Stop", on_click=handle_stop),
                            ft.Button("Next", on_click=handle_next),
                            ft.Button("Previous", on_click=handle_previous),
                            ft.Button("Seek s=10", on_click=handle_seek),
                            ft.Button("Jump to first Media", on_click=handle_jump),
                            ft.Button("Add Random Media", on_click=handle_add_media),
                            ft.Button(
                                "Remove Random Media", on_click=handle_remove_media
                            ),
                            ft.Button("Enter Fullscreen", on_click=handle_fullscreen),
                        ],
                    ),
                    ft.Slider(
                        min=0,
                        value=100,
                        max=100,
                        label="Volume = {value}%",
                        divisions=10,
                        width=400,
                        on_change=handle_volume_change,
                    ),
                    ft.Slider(
                        min=1,
                        value=1,
                        max=3,
                        label="Playback rate = {value}X",
                        divisions=6,
                        width=400,
                        on_change=handle_playback_rate_change,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
