---
class_name: flet_video.Video
examples: ../../examples/controls/video
---

# Video

Embed a full-featured video player in your [Flet](https://flet.dev) app with playlist support, hardware acceleration controls, and subtitle configuration.

It is powered by the [media_kit](https://pub.dev/packages/media_kit) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

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

## Requirements

The below sections show the required configurations for each platform.

### Android

You may need to declare and request file-system/storage permissions, depending on your use case:

- [`android.permission.READ_MEDIA_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#READ_MEDIA_AUDIO) (optional): Allows to read audio files from external storage. Android 13 or higher.
- [`android.permission.READ_MEDIA_VIDEO`](https://developer.android.com/reference/android/Manifest.permission#READ_MEDIA_VIDEO) (optional): Allows to read video files from external storage. Android 13 or higher.
- [`android.permission.READ_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#READ_EXTERNAL_STORAGE) (optional): Allows reading from external storage. Android 12 or lower.
- [`android.permission.WRITE_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE) (optional): Allows writing to external storage. Android 12 or lower.

/// tab | `flet build`
```bash
flet build apk \
  --android-permissions android.permission.READ_MEDIA_AUDIO=true \
  --android-permissions android.permission.READ_MEDIA_VIDEO=true \
  --android-permissions android.permission.READ_EXTERNAL_STORAGE=true \
  --android-permissions android.permission.WRITE_EXTERNAL_STORAGE=true
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.permission]
"android.permission.READ_MEDIA_AUDIO" = true
"android.permission.READ_MEDIA_VIDEO" = true
"android.permission.READ_EXTERNAL_STORAGE" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
```
///

Use [`PermissionHandler`][flet_permission_handler.PermissionHandler] to **request** permissions at runtime.

See also:

- [setting Android permissions](../publish/android.md#permissions)

### Linux

[`libmpv`](https://github.com/mpv-player/mpv) libraries must be installed and present on the machine running the app.

On Ubuntu/Debian, this can be done with:
```bash
sudo apt install libmpv-dev mpv
```

If you encounter `libmpv.so.1` load errors, run:

```bash
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
```

## Examples

### Basic example

```python
--8<-- "{{ examples }}/example_1/main.py"
```

## Description

{{ class_all_options(class_name) }}
