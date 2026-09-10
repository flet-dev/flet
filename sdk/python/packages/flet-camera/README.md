# flet-camera

[![pypi](https://img.shields.io/pypi/v/flet-camera.svg)](https://pypi.python.org/pypi/flet-camera)
[![downloads](https://static.pepy.tech/badge/flet-camera/month)](https://pepy.tech/project/flet-camera)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-camera)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-camera.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-camera.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-camera/LICENSE)

A camera control for [Flet](https://flet.dev) apps.

> **[Try flet-camera in Flet Studio](https://studio.flet.dev/gallery/media/camera/example/extensions/camera/camera_playground)**
>
> Write, run, and share Python apps in your browser. Start from an example, write your own code, or get help from the AI agent. No installation required.

It is powered by the [camera](https://pub.dev/packages/camera) Flutter package.

## Documentation

Detailed documentation for this package can be found [here](https://flet.dev/docs/controls/camera/).

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
