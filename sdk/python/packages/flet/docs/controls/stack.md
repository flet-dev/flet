::: flet.Stack

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/stack)

### Transparent title over an image

<img src="/img/docs/controls/stack/image-title.png" className="screenshot-50" />

```python
import flet as ft

def main(page: ft.Page):
    st = ft.Stack(
        [
            ft.Image(
                src=f"https://picsum.photos/300/300",
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Row(
                [
                    ft.Text(
                        "Image title",
                        color="white",
                        size=40,
                        weight="bold",
                        opacity=0.5,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        width=300,
        height=300,
    )

    page.add(st)

ft.run(main)
```



### Avatar with online status

<img src="/img/docs/controls/stack/avatar-with-status.png" className="screenshot-10"/>



```python
import flet as ft

def main(page):
    page.add(
        ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )
    )

ft.run(main, view=ft.AppView.WEB_BROWSER)
```



### Absolute positioning inside Stack

<img src="/img/docs/controls/stack/absolute-positioned.png" className="screenshot-50"/>



```python
import flet as ft

def main(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Container(
            ft.Stack(
                [
                    ft.Container(width=20, height=20, bgcolor=ft.Colors.RED, border_radius=5),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.YELLOW,
                        border_radius=5,
                        right=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.BLUE,
                        border_radius=5,
                        right=0,
                        bottom=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.GREEN,
                        border_radius=5,
                        left=0,
                        bottom=0,
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                width=20,
                                height=20,
                                bgcolor=ft.Colors.PURPLE,
                                border_radius=5,
                            )
                        ],
                        left=35,
                        top=35,
                    ),
                ]
            ),
            border_radius=8,
            padding=5,
            width=100,
            height=100,
            bgcolor=ft.Colors.BLACK,
        )
    )

ft.run(main)
```


