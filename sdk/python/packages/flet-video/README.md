# flet-video

[![pypi](https://img.shields.io/pypi/v/flet-video.svg)](https://pypi.python.org/pypi/flet-video)
[![downloads](https://static.pepy.tech/badge/flet-video/month)](https://pepy.tech/project/flet-video)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-video/LICENSE)

A cross-platform video player for [Flet](https://flet.dev) apps.

It is based on the [media_kit](https://pub.dev/packages/media_kit) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/video/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-video` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-video
    ```

- Using `pip`:
    ```bash
    pip install flet-video
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

> [!NOTE]
> To play video on Linux/WSL you need to install [`libmpv`](https://github.com/mpv-player/mpv) library:
>
> ```bash
> sudo apt update
> sudo apt install libmpv-dev libmpv2
> ```
>
> If you encounter `libmpv.so.1` load errors, run:
> 
> ```bash
> sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
> ```

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/controls/video).
