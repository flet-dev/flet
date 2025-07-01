::: flet.CircleAvatar

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/circleavatar)



```python
import flet as ft

def main(page):
    # a "normal" avatar with background image
    a1 = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    # avatar with failing foreground image and fallback text
    a2 = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    # avatar with icon, aka icon with inverse background
    a3 = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.ABC),
    )
    # avatar with icon and custom colors
    a4 = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.WARNING_ROUNDED),
        color=ft.Colors.YELLOW_200,
        bgcolor=ft.Colors.AMBER_700,
    )
    # avatar with online status
    a5 = ft.Stack(
        [
            ft.CircleAvatar(
                foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
            ),
            ft.Container(
                content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                alignment=ft.alignment.bottom_left,
            ),
        ],
        width=40,
        height=40,
    )
    page.add(a1, a2, a3, a4, a5)


ft.run(main)
```


<img src="/img/docs/controls/circle-avatar/circle-avatar.png" className="screenshot-10" />
