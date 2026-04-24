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


async def main(page: ft.Page):
    page.spacing = 20

    video = ft.Ref[ftv.Video]()
    title = ft.Ref[ft.Text]()

    async def handle_pause(e: ft.Event[ft.Button]):
        await video.current.pause()

    async def handle_play_or_pause(e: ft.Event[ft.Button]):
        await video.current.play_or_pause()

    async def handle_play(e: ft.Event[ft.Button]):
        await video.current.play()

    async def handle_stop(e: ft.Event[ft.Button]):
        await video.current.stop()

    async def handle_next(e: ft.Event[ft.Button]):
        await video.current.next()

    async def handle_previous(e: ft.Event[ft.Button]):
        await video.current.previous()

    def handle_track_change(e: ft.Event[ftv.Video]):
        title.current.value = sample_media[e.data].resource

    page.add(
        ftv.Video(
            width=640,
            height=360,
            ref=video,
            playlist=sample_media,
            on_track_change=handle_track_change,
            content=ft.Container(
                padding=ft.Padding.all(10),
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.Padding.all(5),
                            border_radius=20,
                            bgcolor=ft.Colors.GREEN_ACCENT_100,
                            content=ft.Text(size=10, value="", ref=title)
                        )
                    ],
                )
            )
        ),
        ft.Row(
            wrap=True,
            controls=[
                ft.Button("Play", on_click=handle_play),
                ft.Button("Pause", on_click=handle_pause),
                ft.Button("Play Or Pause", on_click=handle_play_or_pause),
                ft.Button("Stop", on_click=handle_stop),
                ft.Button("Next", on_click=handle_next),
                ft.Button("Previous", on_click=handle_previous),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
