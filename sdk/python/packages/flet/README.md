# Flet - quickly build interactive apps for web, desktop and mobile in Python

[Flet](https://flet.dev) is a rich User Interface (UI) framework to quickly build interactive web, desktop and mobile apps in Python without prior knowledge of web technologies like HTTP, HTML, CSS or JavaSscript. You build UI with [controls](https://flet.dev/docs/controls) based on [Flutter](https://flutter.dev/) widgets to ensure your programs look cool and professional.

## Requirements

* Python 3.7 or above on Windows, Linux or macOS

## Installation

```
pip install flet
```

## Hello, world!

```python
import flet
from flet import Page, Text

def main(page: Page):
    page.add(Text("Hello, world!"))

flet.app(target=main)
```

Run the sample above and the app will be started in a native OS window:

![Sample app in a browser](https://flet.dev//img/docs/getting-started/flet-counter-macos.png "Sample app in a native window")

Continue with [Python guide](https://flet.dev/docs/getting-started/python) to learn how to make a real app.

Browse for more [Flet examples](https://github.com/flet-dev/examples/tree/main/python).

Join to a conversation on [Flet Discord server](https://discord.gg/dzWXP8SHG8).
