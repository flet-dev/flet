# flet-audio

[![pypi](https://img.shields.io/pypi/v/flet-audio.svg)](https://pypi.python.org/pypi/flet-audio)
[![downloads](https://static.pepy.tech/badge/flet-audio/month)](https://pepy.tech/project/flet-audio)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-audio)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-audio.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-audio.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-audio/LICENSE)

A [Flet](https://flet.dev) extension package for playing audio.

> **[Try flet-audio in Flet Studio](https://studio.flet.dev/gallery/media/audio/example/extensions/audio/audio_playback_controls)**
>
> Create, run, and share Python apps in your browser. Start from an example, write your own code, or get help from the AI agent. No installation required.

It is based on the [audioplayers](https://pub.dev/packages/audioplayers) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/services/audio/).

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
> On Linux, `Audio` is only available in the **full** desktop client. With the default **light** client,
> calls such as [`play()`](https://flet.dev/docs/services/audio#flet_audio.Audio.play) fail with `Timeout waiting for invoke method listener` - set
> [`FLET_DESKTOP_FLAVOR=full`](https://flet.dev/docs/reference/environment-variables#flet_desktop_flavor) or `desktop_flavor = "full"` under `[tool.flet]` in `pyproject.toml`.
>
> The full client needs GStreamer and, because it also contains the `Video` control, `libmpv`.
> On Debian 12+ and Ubuntu 24.04+:
>
> ```bash
> sudo apt install libmpv2 gstreamer1.0-plugins-base gstreamer1.0-plugins-good
> ```
>
> On Debian 11 and Ubuntu 20.04/22.04, install `libmpv1` instead of `libmpv2`. For more formats, also install
> `gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav`.
> If you receive `error while loading shared libraries: libgstapp-1.0.so.0`, GStreamer is not installed.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/extensions/audio).
