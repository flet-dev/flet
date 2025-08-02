import time

import flet as ft

name = "CupertinoTimerPicker example"


def example():
    timer_picker_value_ref = ft.Ref[ft.Text]()

    def handle_timer_picker_change(e):
        val = int(e.data)
        timer_picker_value_ref.current.value = time.strftime(
            "%H:%M:%S", time.gmtime(val)
        )
        e.control.page.update()

    timer_picker = ft.CupertinoTimerPicker(
        value=3600,
        second_interval=10,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS,
        on_change=handle_timer_picker_change,
    )

    return ft.Row(
        tight=True,
        controls=[
            ft.Text("TimerPicker Value:", size=23),
            ft.TextButton(
                content=ft.Text("00:01:10", size=23, ref=timer_picker_value_ref),
                style=ft.ButtonStyle(color=ft.Colors.RED),
                on_click=lambda e: e.control.page.open(
                    ft.CupertinoBottomSheet(
                        timer_picker,
                        height=216,
                        bgcolor=ft.CupertinoColors.SYSTEM_BACKGROUND,
                        padding=ft.Padding.only(top=6),
                    )
                ),
            ),
        ],
    )
