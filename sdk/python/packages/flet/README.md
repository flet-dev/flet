<p align="center">
  <a href="https://flet.dev"><img src="https://raw.githubusercontent.com/flet-dev/flet/refs/heads/main/media/logo/flet-logo.svg" height="150" alt="Flet logo"></a>
</p>

<p align="center">
    <em>Build multi-platform apps in Python. No frontend experience required.</em>
</p>

<p align="center">
    <a href="https://github.com/flet-dev/flet/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/flet-dev/flet.svg" alt="License" /></a>
    <a href="https://pypi.org/project/flet" target="_blank">
        <img src="https://img.shields.io/pypi/v/flet?color=%2334D058&label=pypi" alt="Package version" /></a>
    <a href="https://pepy.tech/project/flet" target="_blank">
        <img src="https://static.pepy.tech/badge/flet/month" alt="Supported Python versions" /></a>
    <a href="https://pypi.org/project/flet" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/flet.svg?color=%2334D058" alt="Supported Python versions" /></a>
    <a href="https://github.com/flet-dev/flet/actions/workflows/ci.yml" target="_blank">
        <img src="https://github.com/flet-dev/flet/actions/workflows/ci.yml/badge.svg" alt="Build status" /></a>
</p>

---

Flet is a framework that allows building mobile, desktop and web applications
in Python only without prior experience in frontend development.

### <img src="https://flet.dev/img/pages/home/single-code-base.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Single code base for any device

Your app will equally look great on iOS, Android, Windows, Linux, macOS and web.

### <img src="https://flet.dev/img/pages/home/python.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Build an entire app in Python

Build a cross-platform app without knowledge of Dart, Swift, Kotlin, HTML or JavaScript - only Python!

### <img src="https://flet.dev/img/pages/home/controls.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;150+ built-in controls and services

Beautiful UI widgets with Material and Cupertino design: layout, navigation, dialogs, charts - Flet uses Flutter to render UI.

### <img src="https://flet.dev/img/pages/home/python-packages.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;50+ Python packages for iOS and Android

Numpy, pandas, pydantic, cryptography, opencv, pillow and other popular libraries.

### <img src="https://flet.dev/img/pages/home/web-support.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Full web support

Flet apps run natively in modern browsers using WebAssembly and Pyodide, with no server required. Prefer server-side? Deploy as a Python web app with real-time UI updates.

### <img src="https://flet.dev/img/pages/home/packaging.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Built-in packaging

Build standalone executables or bundles for iOS, Android, Windows, Linux, macOS and web. Instantly deploy to App Store and Google Play.

### <img src="https://flet.dev/img/pages/home/test-on-ios-android.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Test on iOS and Android

Test your project on your own mobile device with Flet App. See your app updates as you make changes.

### <img src="https://flet.dev/img/pages/home/extensible.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Extensible

Easily wrap any of thousands of Flutter packages to use with Flet or build new controls in pure Python using built-in UI primitives.

### <img src="https://flet.dev/img/pages/home/accessible.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Accessible

Flet is built with Flutter which has solid accessibility foundations on Android, iOS, web, and desktop.

## Flet app example

Below is a simple "Counter" app, with a text field and two buttons to increment and decrement the counter value:

```python title="counter.py"
import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        input.value = str(int(input.value) - 1)

    def plus_click(e):
        input.value = str(int(input.value) + 1)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                input,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
        )
    )

ft.run(main)
```

To run the app, install `flet`:

```bash
pip install 'flet[all]'
```

then launch the app:

```bash
flet run counter.py
```

This will open the app in a native OS window - what a nice alternative to Electron! 🙂

<p align="center">
    <img src="https://docs.flet.dev/assets/getting-started/counter-app/macos.png" width="45%" />
</p>

To run the same app as a web app use `--web` option with `flet run` command:

```bash
flet run --web counter.py
```

<p align="center">
    <img src="https://docs.flet.dev/assets/getting-started/counter-app/safari.png" width="60%" />
</p>

## Learn more

* [Website](https://flet.dev)
* [Documentation](https://docs.flet.dev)
* [Roadmap](https://flet.dev/roadmap)
* [Apps Gallery](https://flet.dev/gallery)

## Community

* [Discussions](https://github.com/flet-dev/flet/discussions)
* [Discord](https://discord.gg/dzWXP8SHG8)
* [X (Twitter)](https://twitter.com/fletdev)
* [Bluesky](https://bsky.app/profile/fletdev.bsky.social)
* [Email us](mailto:hello@flet.dev)

## Contributing

Want to help improve Flet? Check out the [contribution guide](https://docs.flet.dev/contributing).
