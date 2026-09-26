# flet-webview

[![pypi](https://img.shields.io/pypi/v/flet-webview.svg)](https://pypi.python.org/pypi/flet-webview)
[![downloads](https://static.pepy.tech/badge/flet-webview/month)](https://pepy.tech/project/flet-webview)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-webview)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-webview.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-webview.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-webview/LICENSE)

A [Flet](https://flet.dev) extension for displaying web content in a WebView.

> **[Try Flet online in Flet Studio](https://studio.flet.dev/?utm_source=pypi&utm_medium=readme&utm_campaign=flet-webview)**
>
> Create, run, and share Python apps in your browser. Start from an example, write your own code, or get help from the AI agent. No installation required.

It is based on the [webview_all](https://pub.dev/packages/webview_all) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/controls/webview/).

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

Windows requires the Microsoft Edge WebView2 Runtime, and Linux requires `libwebkit2gtk-4.1-0`
(Debian 12, Ubuntu 22.04 and newer). See the [documentation](https://flet.dev/docs/controls/webview/#requirements)
for details.

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

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/extensions/web_view).
