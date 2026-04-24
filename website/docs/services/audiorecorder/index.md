---
class_name: "flet_audio_recorder.AudioRecorder"
examples: "services/audio_recorder"
title: "AudioRecorder"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Audio Recorder

Allows recording audio in [Flet](https://flet.dev) apps.

It is based on the [record](https://pub.dev/packages/record) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

To use `AudioRecorder` service add `flet-audio-recorder` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-audio-recorder
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-audio-recorder  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Requirements

The below sections show the required configurations for each platform.

### Android

Configuration to be made to access the microphone:

- [`android.permission.RECORD_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#RECORD_AUDIO): Allows audio recording.
- [`android.permission.WRITE_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE) (optional): Allows saving your recordings in public folders.
- [`android.permission.MODIFY_AUDIO_SETTINGS`](https://developer.android.com/reference/android/Manifest.permission#MODIFY_AUDIO_SETTINGS) (optional): Allows using bluetooth telephony device like headset/earbuds.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-permissions android.permission.RECORD_AUDIO=true \
  --android-permissions android.permission.WRITE_EXTERNAL_STORAGE=true \
  --android-permissions android.permission.MODIFY_AUDIO_SETTINGS=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.permission]
"android.permission.RECORD_AUDIO" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
"android.permission.MODIFY_AUDIO_SETTINGS" = true
```
</TabItem>
</Tabs>
See also:

- [setting Android permissions](../../publish/android.md#permissions)
- [Audio formats sample rate hints](https://developer.android.com/guide/topics/media/media-formats#audio-formats)

### iOS

Configuration to be made to access the microphone:

- [`NSMicrophoneUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription): Required for recording audio.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build ipa \
  --info-plist NSMicrophoneUsageDescription="Some message to describe why you need this permission..."
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.ios.info]
NSMicrophoneUsageDescription = "Some message to describe why you need this permission..."
```
</TabItem>
</Tabs>
See also:

- [setting iOS permissions](../../publish/ios.md#permissions).

### macOS

Configuration to be made to access the microphone:

- [`NSMicrophoneUsageDescription`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription): Allows recording audio.
- [`com.apple.security.device.audio-input`](https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.security.device.audio-input): Allows recording audio using the built-in microphone and accessing audio input using Core Audio.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos \
  --info-plist NSMicrophoneUsageDescription="Some message to describe why you need this permission..." \
  --macos-entitlements com.apple.security.device.audio-input=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.info]
NSMicrophoneUsageDescription = "Some message to describe why you need this permission..."

[tool.flet.macos.entitlement]
"com.apple.security.device.audio-input" = true
```
</TabItem>
</Tabs>
See also:

- [setting macOS permissions](../../publish/macos.md#permissions)
- [setting macOS entitlements](../../publish/macos.md#entitlements)

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

Additionally/alternatively, you can make use of our predefined cross-platform `microphone`
[permission bundle](../../publish/index.md#predefined-cross-platform-permission-bundles):

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build <target_platform> --permissions microphone
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet]
permissions = ["microphone"]
```
</TabItem>
</Tabs>

## Examples

### Basic recording

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

### Streaming chunks

On web, [`AudioRecorder.stop_recording()`](index.md#flet_audio_recorder.AudioRecorder.stop_recording)
returns a browser-local Blob URL. Use streaming when your app needs access to the recorded bytes.

Set [`AudioRecorderConfiguration.encoder`](types/audiorecorderconfiguration.md#flet_audio_recorder.AudioRecorderConfiguration.encoder)
to [`AudioEncoder.PCM16BITS`](types/audioencoder.md#flet_audio_recorder.AudioEncoder.PCM16BITS)
and handle [`AudioRecorder.on_stream`](index.md#flet_audio_recorder.AudioRecorder.on_stream)
to receive [`AudioRecorderStreamEvent.chunk`](types/audiorecorderstreamevent.md#flet_audio_recorder.AudioRecorderStreamEvent.chunk)
bytes in Python.

[`AudioEncoder.PCM16BITS`](types/audioencoder.md#flet_audio_recorder.AudioEncoder.PCM16BITS)
encoded streams are supported on all platforms. Stream chunks are raw PCM16 bytes and are not directly
playable as an audio file. Wrap the bytes in a container such as WAV in Python when
the destination needs a directly playable recording.

<CodeExample path={frontMatter.examples + '/stream/main.py'} language="python" />

### Streaming upload

Pass [`AudioRecorderUploadSettings`](types/audiorecorderuploadsettings.md) to
[`AudioRecorder.start_recording()`](index.md#flet_audio_recorder.AudioRecorder.start_recording)
to upload [`AudioEncoder.PCM16BITS`](types/audioencoder.md#flet_audio_recorder.AudioEncoder.PCM16BITS)
recording bytes directly while recording.

The uploaded file contains raw PCM16 bytes, so a `.pcm` extension is intentional.
See the [streaming chunks example](#streaming-chunks) for inspiration,
if you need to create a playable WAV file.

:::note
Built-in upload URLs from [`Page.get_upload_url()`](../../controls/page.md#flet.Page.get_upload_url)
require upload storage and a signing key. Run with `upload_dir` and set
[`FLET_SECRET_KEY`](../../reference/environment-variables.md#flet_secret_key).
:::

<CodeExample path={frontMatter.examples + '/upload/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
