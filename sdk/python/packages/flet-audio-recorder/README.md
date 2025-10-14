# flet-audio-recorder

[![pypi](https://img.shields.io/pypi/v/flet-audio-recorder.svg)](https://pypi.python.org/pypi/flet-audio-recorder)
[![downloads](https://static.pepy.tech/badge/flet-audio-recorder/month)](https://pepy.tech/project/flet-audio-recorder)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-audio-recorder/LICENSE)

Adds audio recording support to [Flet](https://flet.dev) apps.

It is based on the [record](https://pub.dev/packages/record) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/audio-recorder/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-audio-recorder` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-audio-recorder
    ```

- Using `pip`:
    ```bash
    pip install flet-audio-recorder
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.


> [!NOTE]
> On Linux, encoding is provided by [fmedia](https://stsaz.github.io/fmedia/) which must be installed separately.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/controls/audio_recorder).
