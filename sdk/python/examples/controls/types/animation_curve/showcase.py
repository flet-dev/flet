import asyncio

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    duration_ms = 1200
    track_width = 248
    racer_size = 26
    lane_padding = 10
    lane_inner_width = track_width
    lane_width = lane_inner_width + lane_padding * 2
    travel_units = (lane_inner_width - racer_size) / racer_size
    card_animations: list = []

    def showcase_card(curve: ft.AnimationCurve) -> ft.Container:
        state = {"forward": False}
        progress = ft.Container(
            width=0,
            height=6,
            border_radius=3,
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            animate=ft.Animation(duration_ms, curve=curve),
        )
        racer = ft.Container(
            width=racer_size,
            height=racer_size,
            border_radius=13,
            bgcolor=ft.Colors.PRIMARY,
            shadow=ft.BoxShadow(
                blur_radius=12, spread_radius=1, color=ft.Colors.PRIMARY
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(ft.Icons.BOLT, size=14, color=ft.Colors.ON_PRIMARY),
            offset=ft.Offset(0, 0),
            rotate=0,
            scale=1,
            animate_offset=ft.Animation(duration_ms, curve=curve),
            animate_rotation=ft.Animation(duration_ms, curve=curve),
            animate_scale=ft.Animation(duration_ms, curve=curve),
        )
        status = ft.Text("idle", size=11, color=ft.Colors.ON_SURFACE_VARIANT)

        def animate(forward: bool):
            state["forward"] = forward
            racer.offset = ft.Offset(travel_units if forward else 0, 0)
            racer.rotate = 1 if forward else 0
            racer.scale = 1.25 if forward else 1
            progress.width = track_width if forward else 0
            status.value = "forward" if forward else "reverse"
            racer.update()
            progress.update()
            status.update()

        def replay(e):
            animate(not state["forward"])

        card_animations.append(animate)

        return ft.Container(
            width=340,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=9,
                controls=[
                    ft.Text(curve.name, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        width=track_width,
                        height=6,
                        border_radius=3,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        content=progress,
                    ),
                    ft.Container(
                        width=lane_width,
                        height=48,
                        padding=lane_padding,
                        border=ft.Border.all(1, ft.Colors.OUTLINE),
                        border_radius=8,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        bgcolor=ft.Colors.SURFACE,
                        content=ft.Stack(
                            controls=[
                                ft.Row(
                                    spacing=0,
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Container(
                                            width=4,
                                            height=22,
                                            bgcolor=ft.Colors.OUTLINE,
                                        ),
                                        ft.Container(
                                            width=4,
                                            height=22,
                                            bgcolor=ft.Colors.OUTLINE,
                                        ),
                                    ],
                                ),
                                racer,
                            ],
                        ),
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            status,
                            ft.Button("Replay", icon=ft.Icons.REPLAY, on_click=replay),
                        ],
                    ),
                ],
            ),
        )

    def play_all(e):
        for animate in card_animations:
            animate(True)

    def reverse_all(e):
        for animate in card_animations:
            animate(False)

    async def wave_all():
        for animate in card_animations:
            animate(True)
            await asyncio.sleep(0.04)

    page.appbar = ft.AppBar(title="AnimationCurve Showcase")
    page.add(
        ft.Text(
            "Curve Lab: compare timing profiles across motion, progress, and spin."
        ),
        ft.Row(
            wrap=True,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Button("Play all", icon=ft.Icons.PLAY_ARROW, on_click=play_all),
                ft.Button("Reverse all", icon=ft.Icons.REPLAY, on_click=reverse_all),
                ft.Button("Wave", on_click=lambda e: page.run_task(wave_all)),
            ],
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(curve) for curve in ft.AnimationCurve],
        ),
    )


ft.run(main)
