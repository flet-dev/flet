---
class_name: "flet_camera.Camera"
examples: "controls/camera"
title: "Camera"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Camera

Display a live camera preview, capture photos and videos, and stream camera frames directly in your Flet apps.

Powered by the [camera](https://pub.dev/packages/camera) Flutter package.

## Platform Support

| Platform  | iOS | Android | Web | Windows | macOS | Linux |
|-----------|-----|---------|-----|---------|-------|-------|
| Supported | ✅   | ✅       | ✅   | ❌       | ❌     | ❌     |

## Usage

Add the `flet-camera` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-camera
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-camera  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
:::tip[Permissions]
Request camera (and microphone if recording video with audio) permissions on mobile platforms before initializing the control. You can use [`PermissionHandler`](../../services/permissionhandler/index.md) to prompt the user.
You can also use [predefined cross-platform permission bundles](../../publish/index.md#predefined-cross-platform-permission-bundles) for camera and microphone permissions.
:::

## Requirements

The below sections show the required configurations for each platform.

### Android

Configuration to be made to access the camera and optionally the microphone:

- [`android.permission.CAMERA`](https://developer.android.com/reference/android/Manifest.permission#CAMERA): Allows camera usage.
- [`android.permission.RECORD_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#RECORD_AUDIO) (optional): Allows video recording with audio.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-permissions android.permission.CAMERA=true \
  --android-permissions android.permission.RECORD_AUDIO=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.permission]
"android.permission.CAMERA" = true
"android.permission.RECORD_AUDIO" = true
```
</TabItem>
</Tabs>
See also:

- [setting Android permissions](../../publish/android.md#permissions)

### iOS

Configuration to be made to access the camera and optionally the microphone:

- [`NSCameraUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSCameraUsageDescription): Required for camera usage.
- [`NSMicrophoneUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription) (optional): Required only for video recording with audio. For example, when `enable_audio` parameter of [`Camera.initialize`](index.md#flet_camera.Camera.initialize) is set to `True` (default).

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build ipa \
  --info-plist NSCameraUsageDescription="Some message to describe why you need this permission..." \
  --info-plist NSMicrophoneUsageDescription="Some message to describe why you need this permission..."
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.ios.info]
NSCameraUsageDescription = "Some message to describe why you need this permission..."
NSMicrophoneUsageDescription = "Some message to describe why you need this permission..."
```
</TabItem>
</Tabs>
See also:

- [setting iOS permissions](../../publish/ios.md#permissions)

### Cross-platform

Additionally/alternatively, you can make use of our predefined cross-platform `camera` (and optionally `microphone`)
[permission bundles](../../publish/index.md#predefined-cross-platform-permission-bundles):

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build <target_platform> --permissions camera microphone
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet]
permissions = ["camera", "microphone"]
```
</TabItem>
</Tabs>
## Example

<CodeExample path={frontMatter.examples + '/example_1/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
