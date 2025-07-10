::: flet.ElevatedButton
## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/elevatedbutton)

### Basic elevated buttons



```python
import flet as ft

def main(page: ft.Page):
    page.title = "Basic elevated buttons"
    page.add(
        ft.ElevatedButton(text="Elevated button"),
        ft.Button("Disabled button", disabled=True),
    )

ft.run(main)
```

<img src="/img/docs/controls/elevated-button/basic-elevated-buttons.png" className="screenshot-20" />

### Elevated buttons with icons



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Elevated buttons with icons"
    page.add(
        ft.ElevatedButton("Button with icon", icon="chair_outlined"),
        ft.ElevatedButton(
            "Button with colorful icon",
            icon="park_rounded",
            icon_color="green400",
        ),
    )

ft.run(main)
```

<img src="/img/docs/controls/elevated-button/elevated-buttons-with-icons.png" className="screenshot-30" />

### Elevated button with `click` event



```python
import flet as ft

def main(page: ft.Page):
    page.title = "Elevated button with 'click' event"

    def button_clicked(e):
        b.data += 1
        t.value = f"Button clicked {b.data} time(s)"
        page.update()

    b = ft.ElevatedButton("Button with 'click' event", on_click=button_clicked, data=0)
    t = ft.Text()

    page.add(b, t)

ft.run(main)
```

<img src="/img/docs/controls/elevated-button/elevated-button-with-click-event.gif" className="screenshot-50" />

### Elevated button with custom content 



```python
import flet as ft

def main(page: ft.Page):
    page.title = "Elevated buttons with custom content"
    page.add(
        ft.ElevatedButton(
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
        ft.ElevatedButton(
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


<img src="/img/docs/controls/elevated-button/elevated-buttons-with-custom-content.png" className="screenshot-30" />

