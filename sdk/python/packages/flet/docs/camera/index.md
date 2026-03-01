---
class_name: flet_camera.Camera
examples: ../../examples/controls/camera
---

# Camera

Display a live camera preview, capture photos and videos, and stream camera frames directly in your Flet apps.

Powered by the [camera](https://pub.dev/packages/camera) Flutter package.

## Platform Support

| Platform  | iOS | Android | Web | Windows | macOS | Linux |
|-----------|-----|---------|-----|---------|-------|-------|
| Supported | ✅   | ✅       | ✅   | ❌       | ❌     | ❌     |

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

## Requirements

The below sections show the required configurations for each platform.

### Android

Configuration to be made to access the camera and optionally the microphone:

- [`android.permission.CAMERA`](https://developer.android.com/reference/android/Manifest.permission#CAMERA): Allows camera usage.
- [`android.permission.RECORD_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#RECORD_AUDIO) (optional): Allows video recording with audio.

/// tab | `flet build`
```bash
flet build apk \
  --android-permissions android.permission.CAMERA=True \
      android.permission.RECORD_AUDIO=True
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.permission]
"android.permission.CAMERA" = true
"android.permission.RECORD_AUDIO" = true
```
///

See also:
- [setting Android permissions](../publish/android.md#permissions)

### iOS

Configuration to be made to access the camera and optionally the microphone:

- [`NSCameraUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSCameraUsageDescription): Required for camera usage.
- [`NSMicrophoneUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription) (optional): Required only for video recording with audio. For example, when `enable_audio` parameter of [`Camera.initialize`][flet_camera.Camera.initialize] is set to `True` (default).

/// tab | `flet build`
```bash
flet build ipa \
  --info-plist NSCameraUsageDescription="Some message to describe why you need this permission..." \
  --info-plist NSMicrophoneUsageDescription="Some message to describe why you need this permission..."
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.ios.info]
NSCameraUsageDescription = "Some message to describe why you need this permission..."
NSMicrophoneUsageDescription = "Some message to describe why you need this permission..."
```
///

See also:
- [setting iOS permissions](../publish/ios.md#permissions)

### Cross-platform

Additionally/Alternatively, you can make use of our predefined cross-platform `camera` (and optionally `microphone`)
[permission bundles](../publish/index.md#predefined-cross-platform-permission-bundles):

/// tab | `flet build`
```bash
flet build <target_platform> --permissions camera microphone
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
permissions = ["camera", "microphone"]
```
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
