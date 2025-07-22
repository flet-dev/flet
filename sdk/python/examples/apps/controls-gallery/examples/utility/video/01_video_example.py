import flet as ft

name = "Video example"


def example():
    sample_media = [
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
        ),
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
        ),
        ft.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
        ),
    ]
    video = ft.Video(
        expand=True,
        playlist=sample_media,
        playlist_mode=ft.PlaylistMode.LOOP,
        fill_color=ft.Colors.BLUE_400,
        aspect_ratio=16 / 9,
        volume=100,
        autoplay=False,
        filter_quality=ft.FilterQuality.HIGH,
        muted=False,
        on_loaded=lambda e: print("Video loaded successfully!"),
        on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
        on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
    )

    return ft.Column(
        height=400,
        expand=True,
        controls=[video],
    )
