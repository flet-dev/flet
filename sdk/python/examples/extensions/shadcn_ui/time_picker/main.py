import datetime

import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn TimePicker"

    def show_meeting(value: datetime.time | None):
        meeting.value = f"Meeting at {value.strftime('%H:%M') if value else '--:--'}"

    def show_alarm(value: datetime.time | None):
        # value is always 24-hour time, even though the picker shows AM/PM.
        alarm.value = (
            f"Alarm at {value.strftime('%H:%M')} ({value.strftime('%I:%M %p')})"
            if value
            else "Alarm not set"
        )

    def set_noon(e: ft.Event[shad.Button]):
        meeting_picker.value = datetime.time(12, 0)
        show_meeting(meeting_picker.value)

    meeting_picker = shad.TimePicker(
        value=datetime.time(14, 30),
        on_change=lambda e: show_meeting(e.control.value),
    )
    meeting = ft.Text()
    show_meeting(meeting_picker.value)

    alarm_picker = shad.TimePicker(
        value=datetime.time(7, 0),
        period=True,
        on_change=lambda e: show_alarm(e.control.value),
    )
    alarm = ft.Text()
    show_alarm(alarm_picker.value)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(
                        "Type hours and minutes into the boxes.",
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Text("24-hour clock", weight=ft.FontWeight.W_600),
                    meeting_picker,
                    meeting,
                    shad.Button(
                        "Set to noon",
                        variant=shad.ButtonVariant.OUTLINE,
                        on_click=set_noon,
                    ),
                    shad.Separator(),
                    ft.Text("12-hour clock", weight=ft.FontWeight.W_600),
                    alarm_picker,
                    alarm,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
