::: flet.OutlinedButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/outlinedbutton)

### Basic outlined buttons



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Basic outlined buttons"
    page.add(
        ft.OutlinedButton(text="Outlined button"),
        ft.OutlinedButton("Disabled button", disabled=True),
    )

ft.run(main)
```

<img src="/img/docs/controls/outlined-button/basic-outlined-buttons.png" className="screenshot-40" />

### Outlined buttons with icons



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Outlined buttons with icons"
    page.add(
        ft.OutlinedButton("Button with icon", icon="chair_outlined"),
        ft.OutlinedButton(
            "Button with colorful icon",
            icon="park_rounded",
            icon_color="green400",
        ),
    )

ft.run(main)
```

<img src="/img/docs/controls/outlined-button/outlined-buttons-with-icons.png" className="screenshot-50" />

### Outlined button with `click` event



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Outlined button with 'click' event"

    def button_clicked(e):
        b.data += 1
        t.value = f"Button clicked {b.data} time(s)"
        page.update()

    b = ft.OutlinedButton("Button with 'click' event", on_click=button_clicked, data=0)
    t = ft.Text()

    page.add(b, t)

ft.run(main)
```

<img src="/img/docs/controls/outlined-button/outlined-button-with-click-event.gif" className="screenshot-50" />

### Outlined button with custom content 



```python
import flet as ft

def main(page: ft.Page):
    page.title = "Outlined buttons with custom content"
    page.add(
        ft.OutlinedButton(
            width=150,
            content=ft.Row(
                [
                    ft.Icon(name=ft.Icons.FAVORITE, color="pink"),
                    ft.Icon(name=ft.Icons.AUDIOTRACK, color="green"),
                    ft.Icon(name=ft.Icons.BEACH_ACCESS, color="blue"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
        ),
        ft.OutlinedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="Compound button", size=20),
                        ft.Text(value="This is secondary text"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
        ),
    )

ft.run(main)

```


<img src="/img/docs/controls/outlined-button/outlined-buttons-with-custom-content.png" className="screenshot-50" />
