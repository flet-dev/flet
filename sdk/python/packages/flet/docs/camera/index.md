---
class_name: flet_camera.Camera
examples: ../../examples/controls/camera
---

# Camera

Display a live camera preview, capture photos and videos, and stream camera frames directly in your Flet apps.

Powered by the [camera](https://pub.dev/packages/camera) Flutter package.

## Platform Support

| Platform | iOS | Android | Web | Windows | macOS | Linux |
|----------|-----|---------|-----|---------|-------|-------|
| Supported|  ✅  |    ✅    |  ✅  |    ❌    |   ❌   |   ❌   |

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
Request camera (and microphone if recording video with audio) permissions on mobile platforms before initializing the control. You can use [`PermissionHandler`][flet_permission_handler.PermissionHandler] to prompt the user.
You can also use [predefined cross-platform permission bundles](../publish/index.md#predefined-cross-platform-permission-bundles) for camera and microphone permissions.
///

### iOS required `Info.plist` keys

Add these entries when building for iOS:

```toml
[tool.flet.ios.info]
NSCameraUsageDescription = "This app uses the camera to capture photos and video."
NSMicrophoneUsageDescription = "This app uses the microphone when recording video with audio."
```

- `NSCameraUsageDescription` is required for camera preview/capture.
- `NSMicrophoneUsageDescription` is required when `enable_audio=True` for video recording.

See also: [iOS permissions](../publish/ios.md#permissions).

### Android required permissions

For Android, enable camera permission, and microphone permission if recording video with audio:

```toml
[tool.flet.android.permission]
"android.permission.CAMERA" = true
"android.permission.RECORD_AUDIO" = true
```

- `android.permission.CAMERA` is required for camera usage.
- `android.permission.RECORD_AUDIO` is required only for video recording with audio.

See also: [Android permissions](../publish/android.md#permissions).

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
