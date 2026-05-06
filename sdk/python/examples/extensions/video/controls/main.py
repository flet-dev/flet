import flet as ft
import flet_video as ftv


def main(page: ft.Page):
    def set_controls(
        value: ftv.VideoControls | ft.Control | None,
    ):
        video.controls = value

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    video := ftv.Video(
                        expand=True,
                        playlist=[
                            ftv.VideoMedia(
                                "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                            ),
                        ],
                        controls=ftv.MaterialDesktopVideoControls(
                            visible_on_mount=True,
                            display_seek_bar=True,
                            modify_volume_on_scroll=True,
                            toggle_fullscreen_on_double_press=True,
                            play_and_pause_on_tap=True,
                            seek_bar_position_color=ft.Colors.BLUE,
                            volume_bar_active_color=ft.Colors.YELLOW,
                            controls_hover_duration=ft.Duration(seconds=5),
                        ),
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Button(
                                "Adaptive",
                                on_click=lambda _: set_controls(
                                    ftv.AdaptiveVideoControls(
                                        material=ftv.MaterialVideoControls(
                                            visible_on_mount=True,
                                            display_seek_bar=True,
                                            volume_gesture=True,
                                            brightness_gesture=True,
                                            seek_gesture=True,
                                            seek_on_double_tap=True,
                                            speed_up_on_long_press=True,
                                            seek_bar_position_color=ft.Colors.BLUE,
                                            button_bar_button_color="#E0F7FA",
                                        ),
                                        material_desktop=ftv.MaterialDesktopVideoControls(
                                            visible_on_mount=True,
                                            display_seek_bar=True,
                                            modify_volume_on_scroll=True,
                                            toggle_fullscreen_on_double_press=True,
                                            play_and_pause_on_tap=True,
                                            hide_mouse_on_controls_removal=True,
                                            seek_bar_position_color=ft.Colors.BLUE,
                                            volume_bar_active_color=ft.Colors.YELLOW,
                                        ),
                                    )
                                ),
                            ),
                            ft.Button(
                                "Material",
                                on_click=lambda _: set_controls(
                                    ftv.MaterialVideoControls(
                                        visible_on_mount=True,
                                        volume_gesture=True,
                                        brightness_gesture=True,
                                        seek_gesture=True,
                                        seek_on_double_tap=True,
                                        speed_up_on_long_press=True,
                                        speed_up_factor=2.5,
                                        controls_transition_duration=ft.Duration(
                                            milliseconds=450
                                        ),
                                        seek_bar_position_color=ft.Colors.BLUE,
                                        button_bar_button_color="#E0F7FA",
                                    )
                                ),
                            ),
                            ft.Button(
                                "Material Desktop",
                                on_click=lambda _: set_controls(
                                    ftv.MaterialDesktopVideoControls(
                                        visible_on_mount=True,
                                        display_seek_bar=True,
                                        modify_volume_on_scroll=True,
                                        toggle_fullscreen_on_double_press=True,
                                        play_and_pause_on_tap=True,
                                        hide_mouse_on_controls_removal=True,
                                        controls_hover_duration=ft.Duration(seconds=5),
                                        seek_bar_position_color=ft.Colors.BLUE,
                                        seek_bar_hover_height=8,
                                        volume_bar_active_color=ft.Colors.YELLOW,
                                    )
                                ),
                            ),
                            ft.Button(
                                "Custom Control",
                                on_click=lambda _: set_controls(
                                    ft.Container(
                                        alignment=ft.Alignment.BOTTOM_CENTER,
                                        padding=16,
                                        content=ft.Text("This is a custom control..."),
                                    )
                                ),
                            ),
                            ft.Button(
                                "No Controls",
                                on_click=lambda _: set_controls(None),
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
