import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    async def handle_screenshot(e: ft.Event[ft.FloatingActionButton]):
        image = await video.take_screenshot(format="image/png")
        if image is None:
            status.value = "No video frame is available yet."
        else:
            preview.content = ft.Image(
                src=image,
                width=260,
                height=146,
                fit=ft.BoxFit.CONTAIN,
            )
            status.value = f"Captured {len(image)} bytes."
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        content="Take screenshot",
        icon=ft.Icons.CAMERA_ALT,
        on_click=handle_screenshot,
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
                        autoplay=True,
                        playlist=[
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                            ),
                        ],
                    ),
                    preview := ft.Container(
                        width=260,
                        height=146,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=ft.Colors.BLACK_12,
                        content=ft.Text("No screenshot yet"),
                    ),
                    status := ft.Text(),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
