::: flet.CupertinoDialogAction

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/cupertinodialogaction)

### CupertinoAlertDialog example



```python
import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def dialog_dismissed(e):
        page.add(ft.Text("Dialog dismissed"))

    def handle_action_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.text}"))
        page.close(cupertino_alert_dialog)

    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Cupertino Alert Dialog"),
        content=ft.Text("Do you want to delete this file?"),
        on_dismiss=dialog_dismissed,
        actions=[
            ft.CupertinoDialogAction(
                text="Yes",
                is_destructive_action=True,
                on_click=handle_action_click,
            ),
            ft.CupertinoDialogAction(
                text="No", 
                is_default_action=True, 
                on_click=handle_action_click
            ),
        ],
    )

    page.add(
        ft.CupertinoFilledButton(
            text="Open CupertinoAlertDialog",
            on_click=lambda e: page.open(cupertino_alert_dialog),
        )
    )


ft.run(main)
```

<img src="/img/docs/controls/cupertinodialogaction/cupertinoalertdialog.png" className="screenshot-50" />

## 