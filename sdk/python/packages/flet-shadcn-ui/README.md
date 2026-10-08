# flet-shadcn-ui

[![pypi](https://img.shields.io/pypi/v/flet-shadcn-ui.svg)](https://pypi.python.org/pypi/flet-shadcn-ui)
[![downloads](https://static.pepy.tech/badge/flet-shadcn-ui/month)](https://pepy.tech/project/flet-shadcn-ui)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-shadcn-ui)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-shadcn-ui.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-shadcn-ui.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-shadcn-ui/LICENSE)

A [Flet](https://flet.dev) extension package with [Shadcn](https://ui.shadcn.com)-styled
controls and [Lucide](https://lucide.dev) icons.

It is based on the [shadcn_ui](https://pub.dev/packages/shadcn_ui) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/controls/shadcnui/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-shadcn-ui` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-shadcn-ui
    ```

- Using `pip`:
    ```bash
    pip install flet-shadcn-ui
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Example

```python
import flet as ft
import flet_shadcn_ui as shad


def main(page: ft.Page):
    page.add(
        shad.Button(
            "Continue",
            leading=shad.LucideIcons.ARROW_RIGHT,
            on_click=lambda e: print("clicked"),
        )
    )


ft.run(main)
```

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/extensions/shadcn_ui).
