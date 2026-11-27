# flet-fluent-ui

[![pypi](https://img.shields.io/pypi/v/flet-fluent-ui.svg)](https://pypi.python.org/pypi/flet-fluent-ui)
[![downloads](https://static.pepy.tech/badge/flet-fluent-ui/month)](https://pepy.tech/project/flet-fluent-ui)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-fluent-ui)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-fluent-ui.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-fluent-ui.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-fluent-ui/LICENSE)

A [Flet](https://flet.dev) extension package with controls styled after Microsoft's
[Fluent Design](https://fluent2.microsoft.design) for Windows, and the Fluent icon set.

It is based on the [fluent_ui](https://pub.dev/packages/fluent_ui) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/controls/fluentui/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-fluent-ui` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-fluent-ui
    ```

- Using `pip`:
    ```bash
    pip install flet-fluent-ui
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Example

```python
import flet as ft
import flet_fluent_ui as fluent


def main(page: ft.Page):
    page.add(
        fluent.FilledButton(
            "Continue",
            on_click=lambda e: print("clicked"),
        )
    )


ft.run(main)
```

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/extensions/fluent_ui).
