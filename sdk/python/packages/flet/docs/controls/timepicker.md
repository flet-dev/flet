::: flet.TimePicker

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/timepicker)

### Basic time picker



```python
import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e):
        page.add(ft.Text(f"TimePicker change: {time_picker.value}"))

    def handle_dismissal(e):
        page.add(ft.Text(f"TimePicker dismissed: {time_picker.value}"))

    def handle_entry_mode_change(e):
        page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=handle_change,
        on_dismiss=handle_dismissal,
        on_entry_mode_change=handle_entry_mode_change,
    )

    page.add(
        ft.ElevatedButton(
            "Pick time",
            icon=ft.Icons.TIME_TO_LEAVE,
            on_click=lambda _: page.open(time_picker),
        )
    )


ft.run(main)
```


<img src="/img/docs/controls/timepicker/time-picker.png" className="screenshot-50" />
