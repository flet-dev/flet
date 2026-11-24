import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    def handle_load(e: ft.Event[ftv.Video]):
        print("Video loaded")

    def handle_complete(e: ft.Event[ftv.Video]):
        print(f"Track completed: {e.data}")

    def handle_track_change(e: ft.Event[ftv.Video]):
        print(f"Track changed to index {e.data}")

    def handle_position_change(e: ft.Event[ftv.Video]):
        print(f"Position: {e.data.in_milliseconds / 1000:.3f}s")

    def handle_duration_change(e: ft.Event[ftv.Video]):
        print(f"Duration changed: {e.data.in_seconds}s")

    def handle_error(e: ft.Event[ftv.Video]):
        print(f"Error: {e.data}")

    def handle_enter_fullscreen(e: ft.Event[ftv.Video]):
        print("Entered fullscreen")

    def handle_exit_fullscreen(e: ft.Event[ftv.Video]):
        print("Exited fullscreen")

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ftv.Video(
                        expand=True,
                        autoplay=True,
                        on_load=handle_load,
                        on_complete=handle_complete,
                        on_track_change=handle_track_change,
                        on_position_change=handle_position_change,
                        on_duration_change=handle_duration_change,
                        on_error=handle_error,
                        on_enter_fullscreen=handle_enter_fullscreen,
                        on_exit_fullscreen=handle_exit_fullscreen,
                        playlist=[
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                            ),
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
