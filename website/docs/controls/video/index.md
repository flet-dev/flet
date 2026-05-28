---
class_name: "flet_video.Video"
examples: "extensions/video"
title: "Video"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Video

Embed a full-featured video player in your [Flet](https://flet.dev) app with playlist support, hardware acceleration controls, and subtitle configuration.

It is powered by the [media_kit](https://pub.dev/packages/media_kit) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add the `flet-video` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-video
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-video  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Requirements

The below sections show the required configurations for each platform.

### Android

You may need to declare and request file-system/storage permissions, depending on your use case:

- [`android.permission.READ_MEDIA_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#READ_MEDIA_AUDIO) (optional): Allows to read audio files from external storage. Android 13 or higher.
- [`android.permission.READ_MEDIA_VIDEO`](https://developer.android.com/reference/android/Manifest.permission#READ_MEDIA_VIDEO) (optional): Allows to read video files from external storage. Android 13 or higher.
- [`android.permission.READ_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#READ_EXTERNAL_STORAGE) (optional): Allows reading from external storage. Android 12 or lower.
- [`android.permission.WRITE_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE) (optional): Allows writing to external storage. Android 12 or lower.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-permissions android.permission.READ_MEDIA_AUDIO=true \
  --android-permissions android.permission.READ_MEDIA_VIDEO=true \
  --android-permissions android.permission.READ_EXTERNAL_STORAGE=true \
  --android-permissions android.permission.WRITE_EXTERNAL_STORAGE=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.permission]
"android.permission.READ_MEDIA_AUDIO" = true
"android.permission.READ_MEDIA_VIDEO" = true
"android.permission.READ_EXTERNAL_STORAGE" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
```
</TabItem>
</Tabs>
Use [`PermissionHandler`](../../services/permissionhandler/index.md) to **request** permissions at runtime.

See also:

- [setting Android permissions](../../publish/android.md#permissions)

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

### Video

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

### Playback

Drive playback programmatically with methods like
[`play()`][flet_video.Video.play], [`pause()`][flet_video.Video.pause], [`stop()`][flet_video.Video.stop], [`seek()`][flet_video.Video.seek], [`next()`][flet_video.Video.next], and [`previous()`][flet_video.Video.previous],
and inspect status with methods like [`is_playing()`][flet_video.Video.is_playing], [`get_current_position()`][flet_video.Video.get_current_position], and [`get_duration()`][flet_video.Video.get_duration].

<CodeExample path={frontMatter.examples + '/playback/main.py'} language="python" />

### Screenshot

Shows how to capture the current video frame with
[`take_screenshot()`][flet_video.Video.take_screenshot] and display it as an image.

<CodeExample path={frontMatter.examples + '/screenshot/main.py'} language="python" />

### Playlist

Mutate [`playlist`][flet_video.Video.playlist] directly to add,
remove, or replace items, and navigate between tracks.

<CodeExample path={frontMatter.examples + '/playlist/main.py'} language="python" />

### Events

Listen for player [events](#flet_video.Video-events) like
[`on_load`][flet_video.Video.on_load], [`on_complete`][flet_video.Video.on_complete], [`on_track_change`][flet_video.Video.on_track_change], etc.

<CodeExample path={frontMatter.examples + '/events/main.py'} language="python" />

### Subtitles

Attach a [`VideoSubtitleTrack`][flet_video.VideoSubtitleTrack] (here, raw VTT text)
and customize its appearance with [`VideoSubtitleConfiguration`][flet_video.VideoSubtitleConfiguration].

<CodeExample path={frontMatter.examples + '/subtitles/main.py'} language="python" />

### Controls

Switch between [`AdaptiveVideoControls`][flet_video.AdaptiveVideoControls], [`MaterialVideoControls`][flet_video.MaterialVideoControls], [`MaterialDesktopVideoControls`][flet_video.MaterialDesktopVideoControls], custom, and hidden control sets at runtime.

<CodeExample path={frontMatter.examples + '/controls/main.py'} language="python" />

### Mode-specific Controls

Show different controls in normal vs. fullscreen mode by mapping each
[`VideoControlsMode`][flet_video.VideoControlsMode] to its own [`controls`][flet_video.Video.controls] value.

<CodeExample path={frontMatter.examples + '/controls_mode/main.py'} language="python" />

### Button Bars

Customize the [`primary_button_bar`][flet_video.MaterialDesktopVideoControls.primary_button_bar],
[`top_button_bar`][flet_video.MaterialDesktopVideoControls.top_button_bar], and
[`bottom_button_bar`][flet_video.MaterialDesktopVideoControls.bottom_button_bar] of
[`MaterialDesktopVideoControls`][flet_video.MaterialDesktopVideoControls] with built-in and custom items.

<CodeExample path={frontMatter.examples + '/button_bars/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
