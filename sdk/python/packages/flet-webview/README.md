# flet-webview

[![pypi](https://img.shields.io/pypi/v/flet-webview.svg)](https://pypi.python.org/pypi/flet-webview)
[![downloads](https://static.pepy.tech/badge/flet-webview/month)](https://pepy.tech/project/flet-webview)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-webview)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-webview.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-webview.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-webview/LICENSE)

A [Flet](https://flet.dev) extension for displaying web content in a WebView.

It is based on the [webview_flutter](https://pub.dev/packages/webview_flutter)
and [webview_flutter_web](https://pub.dev/packages/webview_flutter_web) Flutter packages
on Android, iOS, macOS and web, and on
[webview_all_windows](https://pub.dev/packages/webview_all_windows) and
[webview_all_linux](https://pub.dev/packages/webview_all_linux) on Windows and Linux.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/controls/webview/).

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

> **Platform prerequisites**
>
> - **Linux** requires `libwebkit2gtk-4.1-0`, available from Debian 12 and Ubuntu 22.04 onward.
>   The prebuilt `light` desktop client does not bundle the WebView — use the `full` flavor.
> - **Windows** requires the Edge WebView2 runtime, which ships with Windows 11 and is present on
>   most, but not all, Windows 10 (1809+) installations.

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

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/extensions/webview).
