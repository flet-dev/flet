# flet-audio

[![pypi](https://img.shields.io/pypi/v/flet-audio.svg)](https://pypi.python.org/pypi/flet-audio)
[![downloads](https://static.pepy.tech/badge/flet-audio/month)](https://pepy.tech/project/flet-audio)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-audio/LICENSE)

A [Flet](https://flet.dev) extension package for playing audio.

It is based on the [audioplayers](https://pub.dev/packages/audioplayers) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/audio/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-audio` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-audio
    ```

- Using `pip`:
    ```bash
    pip install flet-audio
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

> [!NOTE]
> On Linux/WSL, you need to install [`GStreamer`](https://github.com/GStreamer/gstreamer) library.
>
> If you receive `error while loading shared libraries: libgstapp-1.0.so.0`, it means `GStreamer` is not installed in your WSL environment.
>
> To install it, run the following command:
>
> ```bash
> apt install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools
> ```

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/controls/audio).
