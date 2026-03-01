import random

import flet as ft


def get_new_image_src() -> str:
    random_id = random.randint(1, 85)
    return f"https://picsum.photos/id/{random_id}/1280/720"


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    initial_src = get_new_image_src()
    image_with_gapless = ft.Image(
        src=initial_src,
        width=340,
        height=220,
        fit=ft.BoxFit.COVER,
        gapless_playback=True,
    )
    image_without_gapless = ft.Image(
        src=initial_src,
        width=340,
        height=220,
        fit=ft.BoxFit.COVER,
        gapless_playback=False,
    )

    def image_panel(title: str, image: ft.Image):
        return ft.Column(
            spacing=8,
            width=340,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=image,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=ft.BorderRadius.all(12),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
            ],
        )

    def next_photo(e: ft.Event[ft.Button]):
        new_src = get_new_image_src()
        image_with_gapless.src = new_src
        image_without_gapless.src = new_src
        page.update()

    page.appbar = ft.AppBar(title="Gapless Playback Showcase")
    page.add(
        ft.Text(
            "Click 'Load next photo' to switch both images to a new URL.\n"
            "The left/top image keeps showing the previous frame while loading the "
            "next one. This is referred to as gapless playback.",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Row(
            wrap=True,
            spacing=20,
            run_spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                image_panel("gapless_playback=True", image_with_gapless),
                image_panel("gapless_playback=False", image_without_gapless),
            ],
        ),
        ft.FilledButton("Load next photo", on_click=next_photo),
    )


ft.run(main)
