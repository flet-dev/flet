---
class_name: flet_video.Video
examples: ../../examples/controls/video
---

# Video

Embed a full-featured video player in your [Flet](https://flet.dev) app with playlist support, hardware acceleration controls, and subtitle configuration.

It is powered by the [media_kit](https://pub.dev/packages/media_kit) Flutter package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add the `flet-video` package to your project dependencies:

/// tab | uv
```bash
uv add flet-video
```

///
/// tab | pip
```bash
pip install flet-video  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Windows Subsystem for Linux (WSL)
    type: note
Install the [`libmpv`](https://github.com/mpv-player/mpv) library when running on WSL.
If you encounter `libmpv.so.1` load errors, run:

```bash
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
```
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
