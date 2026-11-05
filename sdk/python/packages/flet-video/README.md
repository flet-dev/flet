# flet-video

[![pypi](https://img.shields.io/pypi/v/flet-video.svg)](https://pypi.python.org/pypi/flet-video)
[![downloads](https://static.pepy.tech/badge/flet-video/month)](https://pepy.tech/project/flet-video)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-video)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-video.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-video.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-video/LICENSE)

A cross-platform video player for [Flet](https://flet.dev) apps.

> **[Try flet-video in Flet Studio](https://studio.flet.dev/gallery/media/video/example/extensions/video/video)**
>
> Create, run, and share Python apps in your browser. Start from an example, write your own code, or get help from the AI agent. No installation required.

It is based on the [media_kit](https://pub.dev/packages/media_kit) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/controls/video/).

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
> On Linux, `Video` is only available in the **full** desktop client. The default **light** client
> shows `Unknown control: Video` - set [`FLET_DESKTOP_FLAVOR=full`](https://flet.dev/docs/reference/environment-variables#flet_desktop_flavor) or `desktop_flavor = "full"` under
> `[tool.flet]` in `pyproject.toml`.
>
> The full client needs the `libmpv` and GStreamer runtime libraries. On Debian 12+ and Ubuntu 24.04+:
>
> ```bash
> sudo apt install libmpv2 libgstreamer-plugins-base1.0-0
> ```
>
> On Debian 11 and Ubuntu 20.04/22.04, install `libmpv1` instead of `libmpv2`. No `libmpv.so.1` symlink
> is needed. See the [Video docs](https://flet.dev/docs/controls/video#linux) for other distributions.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/extensions/video).
