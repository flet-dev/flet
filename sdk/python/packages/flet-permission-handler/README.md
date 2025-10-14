# flet-permission-handler

[![pypi](https://img.shields.io/pypi/v/flet-permission-handler.svg)](https://pypi.python.org/pypi/flet-permission-handler)
[![downloads](https://static.pepy.tech/badge/flet-permission-handler/month)](https://pepy.tech/project/flet-permission-handler)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-permission-handler/LICENSE)

A [Flet](https://flet.dev) extension that simplifies working with device permissions.

It is based on the [permission_handler](https://pub.dev/packages/permission_handler) Flutter package
and brings similar functionality to Flet, including:

- Requesting permissions at runtime
- Checking the current permission status (e.g., granted, denied)
- Redirecting users to system settings to manually grant permissions

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/permission-handler/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ❌   |   ❌   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-permission-handler` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-permission-handler
    ```

- Using `pip`:
    ```bash
    pip install flet-permission-handler
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/controls/permission_handler).
