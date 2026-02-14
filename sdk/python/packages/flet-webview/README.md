# flet-webview

[![pypi](https://img.shields.io/pypi/v/flet-webview.svg)](https://pypi.python.org/pypi/flet-webview)
[![downloads](https://static.pepy.tech/badge/flet-webview/month)](https://pepy.tech/project/flet-webview)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-webview)
[![docstring coverage](https://raw.githubusercontent.com/flet-dev/flet/main/sdk/python/packages/flet/docs/assets/badges/docs-coverage/flet-webview.svg)](https://github.com/flet-dev/flet/tree/main/sdk/python/packages/flet/docs/assets/badges/docs-coverage)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-webview/LICENSE)

A [Flet](https://flet.dev) extension for displaying web content in a WebView.

It is based on the [webview_flutter](https://pub.dev/packages/webview_flutter)
and [webview_flutter_web](https://pub.dev/packages/webview_flutter_web) Flutter packages.

> **Important:** WebView requires platform-specific configuration (e.g., enabling webview on iOS). Consult Flutter's platform setup guides.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/webview/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ✅   |   ❌   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-webview` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-webview
    ```

- Using `pip`:
    ```bash
    pip install flet-webview
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/examples/controls/webview).
