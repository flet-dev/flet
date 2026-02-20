# flet-camera

[![pypi](https://img.shields.io/pypi/v/flet-camera.svg)](https://pypi.python.org/pypi/flet-camera)
[![downloads](https://static.pepy.tech/badge/flet-camera/month)](https://pepy.tech/project/flet-camera)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-camera)
[![docstring coverage](https://docs.flet.dev/assets/badges/docs-coverage/flet-camera.svg)](https://docs.flet.dev/assets/badges/docs-coverage/flet-camera.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-camera/LICENSE)

A camera control for [Flet](https://flet.dev) apps.

It is powered by the [camera](https://pub.dev/packages/camera) Flutter package.

## Documentation

Detailed documentation for this package can be found [here](https://docs.flet.dev/camera/).

## Platform Support

| Platform | iOS | Android | Web | Windows | macOS | Linux |
|----------|-----|---------|-----|---------|-------|-------|
| Supported|  ✅  |    ✅    |  ✅  |    ❌    |   ❌   |   ❌   |

## Usage

### Installation

To install the `flet-camera` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-camera
    ```

- Using `pip`:
    ```bash
    pip install flet-camera
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Permissions

Camera access requires runtime permissions on mobile and desktop platforms. Use the [`flet-permission-handler`](https://pypi.org/project/flet-permission-handler/) package to request camera and microphone permissions before initializing the control.
