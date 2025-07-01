::: flet.Dismissible

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/dismissible)

### Dismissible ListView Tiles



```python
import flet as ft


def main(page):
    def handle_dlg_action_clicked(e):
        page.close(dlg)
        dlg.data.confirm_dismiss(e.control.data)

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete this item?"),
        actions=[
            ft.TextButton("Yes", data=True, on_click=handle_dlg_action_clicked),
            ft.TextButton("No", data=False, on_click=handle_dlg_action_clicked),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
        if e.direction == ft.DismissDirection.END_TO_START:  # right-to-left slide
            # save current dismissible to dialog's data, for confirmation in handle_dlg_action_clicked
            dlg.data = e.control
            page.open(dlg)
        else:  # left-to-right slide
            e.control.confirm_dismiss(True)

    def handle_dismiss(e):
        e.control.parent.controls.remove(e.control)
        page.update()

    def handle_update(e: ft.DismissibleUpdateEvent):
        print(
            f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}"
        )

    page.add(
        ft.ListView(
            expand=True,
            controls=[
                ft.Dismissible(
                    content=ft.ListTile(title=ft.Text(f"Item {i}")),
                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                    background=ft.Container(bgcolor=ft.Colors.GREEN),
                    secondary_background=ft.Container(bgcolor=ft.Colors.RED),
                    on_dismiss=handle_dismiss,
                    on_update=handle_update,
                    on_confirm_dismiss=handle_confirm_dismiss,
                    dismiss_thresholds={
                        ft.DismissDirection.END_TO_START: 0.2,
                        ft.DismissDirection.START_TO_END: 0.2,
                    },
                )
                for i in range(10)
            ],
        )
    )


ft.run(main)
```


<img src="/img/docs/controls/dismissible/dismissible-listview.gif" className="screenshot-40"/>
