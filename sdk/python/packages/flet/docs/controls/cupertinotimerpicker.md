::: flet.CupertinoTimerPicker

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/cupertinotimerpicker)

### Basic Example

```python
import time
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    timer_picker_value_ref = ft.Ref[ft.Text]()

    def handle_timer_picker_change(e):
        # e.data is the selected time in seconds
        timer_picker_value_ref.current.value = time.strftime("%H:%M:%S", time.gmtime(int(e.data)))
        page.update()

    cupertino_timer_picker = ft.CupertinoTimerPicker(
        value=3600,
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
                    on_click=lambda e: page.open(
                        ft.CupertinoBottomSheet(
                            cupertino_timer_picker,
                            height=216,
                            padding=ft.padding.only(top=6),
                        )
                    ),
                ),
            ],
        ),
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertino-timer-picker/basic-cupertino-timer-picker.gif" className="screenshot-50" />