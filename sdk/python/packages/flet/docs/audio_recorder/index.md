---
class_name: flet_audio_recorder.AudioRecorder
examples: ../../examples/services/audio_recorder
---

# Audio Recorder

Allows recording audio in [Flet](https://flet.dev) apps.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

To use `AudioRecorder` service add `flet-audio-recorder` package to your project dependencies:

/// tab | uv
```bash
uv add flet-audio-recorder
```

///
/// tab | pip
```bash
pip install flet-audio-recorder  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Linux
    type: note
Audio encoding on Linux is provided by [fmedia](https://stsaz.github.io/fmedia/) and must be installed separately.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
