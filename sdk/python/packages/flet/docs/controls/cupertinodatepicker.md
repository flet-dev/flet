::: flet.CupertinoDatePicker

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/cupertinodatepicker)

### Basic Example



```python
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_date_change(e: ft.ControlEvent):
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d %H:%M %p')}"))

    cupertino_date_picker = ft.CupertinoDatePicker(
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
        on_change=handle_date_change,
    )
    page.add(
        ft.CupertinoFilledButton(
            "Open CupertinoDatePicker",
            on_click=lambda e: page.open(
                ft.CupertinoBottomSheet(
                    cupertino_date_picker,
                    height=216,
                    padding=ft.padding.only(top=6),
                )
            ),
        )
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertino-date-picker/basic-cupertino-date-picker.png" className="screenshot-50" />