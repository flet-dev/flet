# Flet

<img src="media/logo/flet-logo.svg" width="50%"/>

[![Build status](https://ci.appveyor.com/api/projects/status/xwablctxslvey576/branch/main?svg=true)](https://ci.appveyor.com/project/flet-dev/flet/branch/main)

Flet is a framework that enables you to easily build realtime web, mobile and desktop apps in your favorite language and securely share them with your team. No frontend experience required.

### ⚡From idea to app in minutes

An internal tool or a dashboard for your team, weekend project, data entry form, kiosk app or high-fidelity prototype - Flet is an ideal framework to quickly hack a great-looking interactive apps to serve a group of users.

### 📐 Simple architecture

No more complex architecture with JavaScript frontend, REST API backend, database, cache, etc. With Flet you just write a monolith stateful app in Python only and get multi-user, realtime Single-Page Application (SPA).

### 🔋Batteries included

To start developing with Flet, you just need your favorite IDE or text editor. No SDKs, no thousands of dependencies, no complex tooling - Flet has built-in web server with assets hosting and desktop clients.

### &nbsp;<img src="media/flutter/icon_flutter.svg" height="20px" />&nbsp;&nbsp;Powered by Flutter

Flet UI is built with [Flutter](https://flutter.dev/), so your app looks professional and could be delivered to any platform. Flet simplifies Flutter model by combining smaller "widgets" to ready-to-use "controls" with imperative programming model.

### 🌐 Speaks your language

Flet is language-agnostic, so anyone on your team could develop Flet apps in their favorite language. [Python](https://flet.dev/docs/guides/python/getting-started) is already supported, Go, C# and others are [coming next](https://flet.dev/docs/roadmap).

### 📱 Deliver to any device

Deploy Flet app as a web app and view it in a browser. Package it as a standalone desktop app for Windows, macOS and Linux. Install it on mobile as [PWA](https://web.dev/what-are-pwas/) or view via Flet app for iOS and Android.

## Flet app example

At the moment you can write Flet apps in Python and other languages will be added soon.

Here is a sample "Counter" app:

```python title="counter.py"
import flet
from flet import IconButton, Page, Row, TextField, icons

def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = "center"

    txt_number = TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        txt_number.value = int(txt_number.value) - 1
        page.update()

    def plus_click(e):
        txt_number.value = int(txt_number.value) + 1
        page.update()

    page.add(
        Row(
            [
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=plus_click),
            ],
            alignment="center",
        )
    )

flet.app(target=main)
```

To run the app install `flet` module:

```bash
pip install flet
```

and run the program:

```bash
python counter.py
```

The app will be started in a native OS window - what a nice alternative to Electron!

<img src="https://flet.dev/img/docs/getting-started/flet-counter-macos.png" width="45%" />


Now, if you want to run the app as a web app, just replace the last line with:

```python
flet.app(target=main, view=flet.WEB_BROWSER)
```

run again and now you instantly get a web app:

<img src="https://flet.dev/img/docs/getting-started/flet-counter-safari.png" width="60%" />

## Getting started

* [Creating Flet apps in Python](https://flet.dev/docs/guides/python/getting-started)
* [Controls reference](https://flet.dev/docs/controls)

## Sample apps in Python

* [Greeter](https://github.com/flet-dev/examples/blob/main/python/apps/greeter/greeter.py)
* [Counter](https://github.com/flet-dev/examples/blob/main/python/apps/counter/counter.py)
* [To-Do](https://github.com/flet-dev/examples/blob/main/python/apps/todo/todo.py)
* [Icons Browser](https://github.com/flet-dev/examples/blob/main/python/apps/icons-browser/main.py) ([Online Demo](https://flet-icons-browser.fly.dev/))

## Community

* [Discussions](https://github.com/flet-dev/flet/discussions)
* [Discord](https://discord.gg/dzWXP8SHG8)
* [Twitter](https://twitter.com/fletdev)
* [Email](mailto:hello@flet.dev)

## Contribute to this wonderful project

* Read the CONTRIBUTE.md file