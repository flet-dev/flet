import flet as ft

PHOTO_IDS = [1003, 1024, 1025, 1031, 1043, 1069]


def photo_url(photo_id: int) -> str:
    return f"https://picsum.photos/id/{photo_id}/1280/720"


def main(page: ft.Page):
    page.title = "Image.gapless_playback example"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    image_index = 0
    current_src = photo_url(PHOTO_IDS[image_index])

    image_with_gapless = ft.Image(
        src=current_src,
        width=340,
        height=220,
        fit=ft.BoxFit.COVER,
        gapless_playback=True,
    )

    image_without_gapless = ft.Image(
        src=current_src,
        width=340,
        height=220,
        fit=ft.BoxFit.COVER,
        gapless_playback=False,
    )

    status_text = ft.Text(f"Photo {image_index + 1} / {len(PHOTO_IDS)}")

    def image_panel(title: str, image: ft.Image):
        return ft.Column(
            [
                ft.Text(title, weight=ft.FontWeight.W_600),
                ft.Container(
                    content=image,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=ft.BorderRadius.all(12),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
            ],
            spacing=8,
            width=340,
        )

    def next_photo(e: ft.Event[ft.Button]):
        nonlocal image_index
        image_index = (image_index + 1) % len(PHOTO_IDS)
        new_src = photo_url(PHOTO_IDS[image_index])
        image_with_gapless.src = new_src
        image_without_gapless.src = new_src
        status_text.value = f"Photo {image_index + 1} / {len(PHOTO_IDS)}"
        page.update()

    page.add(
        ft.Text(
            "Click 'Load next photo' to switch both images to a new URL.\n"
            "The left image keeps showing the previous frame while loading.",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Row(
            [
                image_panel("gapless_playback=True", image_with_gapless),
                image_panel("gapless_playback=False", image_without_gapless),
            ],
            wrap=True,
            spacing=20,
            run_spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        status_text,
        ft.FilledButton("Load next photo", on_click=next_photo),
    )


ft.run(main)
