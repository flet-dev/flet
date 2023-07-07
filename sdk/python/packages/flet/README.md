# Flet - quickly build interactive apps for web, desktop and mobile in Python

[Flet](https://flet.dev) is a rich User Interface (UI) framework to quickly build interactive web, desktop and mobile apps in Python without prior knowledge of web technologies like HTTP, HTML, CSS or JavaSscript. You build UI with [controls](https://flet.dev/docs/controls) based on [Flutter](https://flutter.dev/) widgets to ensure your programs look cool and professional.

## Requirements

* Python 3.7 or above on Windows, Linux or macOS

## Installation

```
pip install flet
```

## Create the app

Create `main.py` file with the following content:

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)
```

## Run as a desktop app

The following command will start the app in a native OS window:

```
flet run main.py
```

![Sample app in a native window](https://flet.dev/img/docs/getting-started/flet-counter-macos.png)

## Run as a web app

The following command will start the app as a web app:

```
flet run --web main.py
```

![Sample app in a browser](https://flet.dev/img/docs/getting-started/flet-counter-safari.png)

## Learn more

Visit [Flet website](https://flet.dev).

Continue with [Python guide](https://flet.dev/docs/getting-started/python) to learn how to make a real app.

Browse for more [Flet examples](https://github.com/flet-dev/examples/tree/main/python).

Join to a conversation on [Flet Discord server](https://discord.gg/dzWXP8SHG8).
