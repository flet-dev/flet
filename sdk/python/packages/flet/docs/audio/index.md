---
class_name: flet_audio.Audio
examples: ../../examples/services/audio
---

# Audio

Allows playing audio in [Flet](https://flet.dev) apps.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

To use `Audio` control add `flet-audio` package to your project dependencies:

/// tab | uv
```bash
uv add flet-audio
```

///
/// tab | pip
```bash
pip install flet-audio  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

/// admonition | Linux/WSL (Windows Subsystem for Linux)
    type: note
To play audio on Linux/WSL you need to install [`GStreamer`](https://github.com/GStreamer/gstreamer) library.

If you receive `error while loading shared libraries: libgstapp-1.0.so.0`,
it means `GStreamer` is not installed in your WSL environment.

To install it, run the following command:

```bash
apt install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools
```
///

## Description

{{ class_all_options(class_name) }}
