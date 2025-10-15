# flet-flashlight

[![pypi](https://img.shields.io/pypi/v/flet-flashlight.svg)](https://pypi.python.org/pypi/flet-flashlight)
[![downloads](https://static.pepy.tech/badge/flet-flashlight/month)](https://pepy.tech/project/flet-flashlight)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-flashlight/LICENSE)

A [Flet](https://flet.dev) extension to manage the device torch/flashlight.

It is based on the [flashlight](https://pub.dev/packages/flashlight) Flutter package.

> **Important:** Add `Flashlight` instances to `page.services` before calling toggle or other methods.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/flashlight/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

## Usage

### Installation

To install the `flet-flashlight` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-flashlight
    ```

- Using `pip`:
    ```bash
    pip install flet-flashlight
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/examples/controls/flashlight).
