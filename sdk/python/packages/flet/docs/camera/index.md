---
class_name: flet_camera.Camera
examples: ../../examples/controls/camera
---

# Camera

Display a live camera preview, capture photos and videos, and stream camera frames directly in your Flet apps.

Powered by the [camera](https://pub.dev/packages/camera) Flutter package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add the `flet-camera` package to your project dependencies:

/// tab | uv
```bash
uv add flet-camera
```

///
/// tab | pip
```bash
pip install flet-camera  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Permissions
    type: tip
Request camera (and microphone if recording video with audio) permissions on mobile and desktop platforms before initializing the control. You can use [`flet-permission-handler`](https://pypi.org/project/flet-permission-handler/) to prompt the user.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
