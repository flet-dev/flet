import flet as ft
import flet_video as ftv


@ft.component
def App():
    fullscreen, set_fullscreen = ft.use_state(False)
    volume, set_volume = ft.use_state(100)
    playback_rate, set_playback_rate = ft.use_state(1.0)

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
        set_volume(e.control.value)

    def handle_playback_rate_change(e: ft.Event[ft.Slider]):
        set_playback_rate(e.control.value)

    async def handle_seek(e: ft.Event[ft.Button]):
        await video.seek(10000)

    async def handle_fullscreen(e: ft.Event[ft.Button]):
        set_fullscreen(True)

    return ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                video := ftv.Video(
                    expand=True,
                    fullscreen=fullscreen,
                    playlist=sample_media[0:2],
                    playlist_mode=ftv.PlaylistMode.LOOP,
                    aspect_ratio=16 / 9,
                    volume=volume,
                    playback_rate=playback_rate,
                    autoplay=False,
                    filter_quality=ft.FilterQuality.HIGH,
                    muted=False,
                    on_load=lambda e: print("Video loaded successfully!"),
                    on_enter_fullscreen=lambda e: set_fullscreen(True),
                    on_exit_fullscreen=lambda e: set_fullscreen(False),
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
                        ft.Button("Enter Fullscreen", on_click=handle_fullscreen),
                    ],
                ),
                ft.Slider(
                    min=0,
                    value=volume,
                    max=100,
                    label="Volume = {value}%",
                    divisions=10,
                    width=400,
                    on_change=handle_volume_change,
                ),
                ft.Slider(
                    min=1,
                    value=playback_rate,
                    max=3,
                    label="Playback rate = {value}X",
                    divisions=6,
                    width=400,
                    on_change=handle_playback_rate_change,
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
