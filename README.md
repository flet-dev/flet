<p align="center">
  <a href="https://flet.dev"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/flet-dev/flet/refs/heads/main/media/logo/flet-logo-dark.svg">
    <img src="https://raw.githubusercontent.com/flet-dev/flet/refs/heads/main/media/logo/flet-logo.svg" height="150" alt="Flet logo">
  </picture></a>
</p>

<p align="center">
    <em>Build cross-platform apps in Python. No frontend experience required.</em>
</p>

<p align="center">
    <a href="https://github.com/flet-dev/flet/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/flet-dev/flet.svg" alt="License" /></a>
    <a href="https://pypi.org/project/flet" target="_blank">
        <img src="https://img.shields.io/pypi/v/flet?color=%2334D058&label=pypi" alt="Package version" /></a>
    <a href="https://pepy.tech/project/flet" target="_blank">
        <img src="https://static.pepy.tech/badge/flet/month" alt="Monthly downloads" /></a>
    <a href="https://pypi.org/project/flet" target="_blank">
        <img src="https://img.shields.io/badge/python-%3E%3D3.10-%2334D058" alt="Python >= 3.10" /></a>
    <a href="https://github.com/flet-dev/flet/actions/workflows/ci.yml" target="_blank">
        <img src="https://github.com/flet-dev/flet/actions/workflows/ci.yml/badge.svg" alt="Build status" /></a>
    <a href="https://github.com/flet-dev/flet/tree/main/website/static/docs/assets/badges/docs-coverage" target="_blank">
        <img src="https://flet.dev/docs/assets/badges/docs-coverage/flet.svg" alt="Docstring coverage" /></a>
</p>

Flet is a Python framework for building web, desktop, and mobile apps without prior experience in frontend development.

> **[Try Flet online in Flet Studio](https://studio.flet.dev)**
>
> Create, run, and share Python apps in your browser. Start from an example, write your own code, or get help from the AI agent. No installation required.

### <img src="website/static/img/pages/home/single-code-base.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;One Python codebase, six platforms

Build your interface and application logic in Python, and run your app on iOS, Android, Windows, macOS, Linux, and web. No Dart, Swift, Kotlin, HTML, or JavaScript required.

### <img src="website/static/img/pages/home/controls.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;150+ built-in controls and services

Create your interface with ready-made layouts, buttons, forms, navigation, and dialogs. Customize colors, typography, and themes, with Material and Cupertino controls to suit your app.

### <img src="website/static/img/pages/home/declarative-ui.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Declarative UI for growing apps

Organize your app into reusable components and let the UI update when application state changes. Prefer changing controls directly? The imperative style is supported too. [Compare the approaches](https://flet.dev/docs/cookbook/declarative-vs-imperative).

### <img src="website/static/img/pages/home/python-packages.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Your Python libraries, on mobile

Use libraries such as NumPy, pandas, Pillow, and cryptography in your mobile apps. Flet provides [prebuilt binary packages](https://pypi.flet.dev) for iOS and Android, so you don't have to compile native dependencies yourself.

### <img src="website/static/img/pages/home/web-support.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Run in the browser or on your server

Run Python directly in the browser with Pyodide and WebAssembly, with no Python server required. Or keep your Python code on a server and deliver real-time UI updates to the browser.

### <img src="website/static/img/pages/home/packaging.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Built-in packaging

Use `flet build` to package your app for desktop, mobile, or web distribution, including the App Store and Google Play. Configure dependencies, icons, and platform settings in your project's `pyproject.toml`.

### <img src="website/static/img/pages/home/app-testing.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Test your app on desktop and mobile

Write [integration tests with pytest](https://flet.dev/docs/getting-started/integration-testing) and run them against your packaged app with `flet test`. Tap buttons, enter text, and verify user flows on desktop and mobile, with screenshot comparisons on Android and iOS.

### <img src="website/static/img/pages/home/ai-assistance.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Build with help from AI

Explore and create apps with the AI agent in [Flet Studio](https://studio.flet.dev), or connect your coding assistant to the [Flet MCP server](https://flet.dev/docs/cookbook/flet-mcp) for version-specific API information and tools to find examples and icons.

### <img src="website/static/img/pages/home/extensible.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Extensible

Build custom controls in Python by composing existing controls, or create extensions that wrap Flutter packages to add new UI components and platform integrations.

### <img src="website/static/img/pages/home/accessible.svg" width="25" align="top" />&nbsp;&nbsp;&nbsp;Accessible

Add screen-reader labels, tooltips, keyboard shortcuts, and custom semantics to help more people use your app. Inspect the accessibility information your UI exposes with the [semantics debugger](https://flet.dev/docs/cookbook/accessibility#debugging-semantics).

## Flet app example

This simple counter app displays a number in the center of the screen. Press the **+** button to increment it:

```python
import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                content=counter,
                alignment=ft.Alignment.CENTER,
            ),
        )
    )


ft.run(main)
```

To run the app, install `flet`:

```bash
pip install 'flet[all]'
```

Save the code as `counter.py`, then launch the app:

```bash
flet run counter.py
```

This opens the app in a native desktop window. The screenshot below shows it after pressing **+** three times:

<p align="center">
    <img src="https://flet.dev/docs/assets/getting-started/counter-app/macos.png" width="45%" />
</p>

To run the same app in your browser, add `--web`:

```bash
flet run --web counter.py
```

<p align="center">
    <img src="https://flet.dev/docs/assets/getting-started/counter-app/safari.png" width="60%" />
</p>

## Learn more

* [Website](https://flet.dev)
* [Documentation](https://flet.dev/docs/)
* [Roadmap](https://flet.dev/roadmap)
* [Apps Gallery](https://studio.flet.dev/gallery)

## Community

* [Discussions](https://github.com/flet-dev/flet/discussions)
* [Discord](https://discord.gg/dzWXP8SHG8)
* [X (Twitter)](https://twitter.com/fletdev)
* [Bluesky](https://bsky.app/profile/fletdev.bsky.social)
* [Email us](mailto:hello@flet.dev)

## Contributing

Want to help improve Flet? Check out the [contribution guide](CONTRIBUTING.md).
