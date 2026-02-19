---
class_name: flet_audio.Audio
examples: ../../examples/services/audio
---

# Audio

Allows playing audio in [Flet](https://flet.dev) apps.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

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

/// admonition | Linux requirements
    type: note
To play audio on Linux (or [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)) you need to
install [`GStreamer`](https://github.com/GStreamer/gstreamer) library.

To install the minimal set of GStreamer libs on Ubuntu/Debian, run:

```bash
sudo apt install libgtk-3-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

To install the full set:

```bash
sudo apt install \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools \
  gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \
  gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

If you receive `error while loading shared libraries: libgstapp-1.0.so.0`,
it means `GStreamer` is not installed in your WSL environment.
Install the full set of GStreamer libs, as shown above.

See [this guide](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c)
for installing on other Linux distributions.
///

## Examples

### Basic example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
