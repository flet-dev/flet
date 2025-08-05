import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    timer_picker_value_ref = ft.Ref[ft.Text]()

    def handle_timer_picker_change(e: ft.Event[ft.CupertinoTimerPicker]):
        timer_picker_value_ref.current.value = time.strftime(
            "%H:%M:%S", time.gmtime(e.data.in_seconds)
        )
        # timer_picker_value_ref.current.value = f"{e.data.in_hours}:{(e.data.in_minutes % 60)}:{(e.data.in_seconds % 60) % 60}"
        page.update()

    timer_picker = ft.CupertinoTimerPicker(
        value=300,
        second_interval=10,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS,
        on_change=handle_timer_picker_change,
    )

    page.add(
        ft.Row(
            tight=True,
            controls=[
                ft.Text("TimerPicker Value:", size=23),
                ft.CupertinoButton(
                    content=ft.Text(
                        ref=timer_picker_value_ref,
                        value="00:01:10",
                        size=23,
                        color=ft.CupertinoColors.DESTRUCTIVE_RED,
                    ),
                    on_click=lambda e: page.show_dialog(
                        ft.CupertinoBottomSheet(
                            content=timer_picker,
                            height=216,
                            padding=ft.Padding.only(top=6),
                        )
                    ),
                ),
            ],
        ),
    )


ft.run(main)
