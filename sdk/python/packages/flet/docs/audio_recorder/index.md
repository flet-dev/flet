---
class_name: flet_audio_recorder.AudioRecorder
examples: ../../examples/services/audio_recorder
---

# Audio Recorder

Allows recording audio in [Flet](https://flet.dev) apps.

It is based on the [record](https://pub.dev/packages/record) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

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

## Requirements

The below sections show the required configurations for each platform.

### Android

Configuration to be made to access the microphone:

- [`android.permission.RECORD_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#RECORD_AUDIO): Allows audio recording.
- [`android.permission.WRITE_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE) (optional): Allows saving your recordings in public folders.
- [`android.permission.MODIFY_AUDIO_SETTINGS`](https://developer.android.com/reference/android/Manifest.permission#MODIFY_AUDIO_SETTINGS) (optional): Allows using bluetooth telephony device like headset/earbuds.

/// tab | `flet build`
```bash
flet build apk \
  --android-permissions android.permission.RECORD_AUDIO=True \
      android.permission.WRITE_EXTERNAL_STORAGE=True \
      android.permission.MODIFY_AUDIO_SETTINGS=True
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.permission]
"android.permission.RECORD_AUDIO" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
"android.permission.MODIFY_AUDIO_SETTINGS" = true
```
///

See also:
- [setting Android permissions](../publish/android.md#permissions)
- [Audio formats sample rate hints](https://developer.android.com/guide/topics/media/media-formats#audio-formats)

### iOS

Configuration to be made to access the microphone:

- [`NSMicrophoneUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription): Required for recording audio.

/// tab | `flet build`
```bash
flet build ipa \
  --info-plist NSMicrophoneUsageDescription="Some message to describe why you need this permission..."
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.ios.info]
NSMicrophoneUsageDescription = "Some message to describe why you need this permission..."
```
///

See also: [setting iOS permissions](../publish/ios.md#permissions).

### macOS

Configuration to be made to access the microphone:

- [`NSMicrophoneUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription): Required for recording audio.
- [`com.apple.security.device.audio-input`](https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.security.device.audio-input) (optional): Required for recording audio.

/// tab | `flet build`
```bash
flet build macos \
  --info-plist NSMicrophoneUsageDescription="Some message to describe why you need this permission..." \
  --entitlement com.apple.security.device.audio-input=True
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.macos.info]
NSMicrophoneUsageDescription = "Some message to describe why you need this permission..."

[tool.flet.macos.entitlement]
"com.apple.security.device.audio-input" = true
```
///

See also:
- [setting macOS permissions](../publish/macos.md#permissions)
- [setting macOS entitlements](../publish/macos.md#entitlements)

### Linux

The following dependencies are required (and widely available on your system):

- `parecord`: Used for audio input.
- `pactl`: Used for utility methods like getting available devices.
- [`ffmpeg`](https://ffmpeg.org): Used for encoding and output.

On Ubuntu 24.04.3 LTS, you can install them using:
```bash
sudo apt install pulseaudio-utils ffmpeg
```

### Cross-platform

Additionally/Alternatively, you can make use of our predefined cross-platform `microphone`
[permission bundle](../publish/index.md#predefined-cross-platform-permission-bundles):

/// tab | `flet build`
```bash
flet build <target_platform> --permissions microphone
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
permissions = ["microphone"]
```
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
