---
class_name: "flet_video.Video"
examples: "extensions/video"
title: "Video"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

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

**No permissions are required** to play media from a URL, from a bundled asset, or
from a file the user picked with [`FilePicker`](../../services/filepicker.md) — the
system picker grants access to the picked file.

You only need media permissions if your app reads media **directly from the device's
shared media library**, without the user picking each file:

- [`android.permission.READ_MEDIA_AUDIO`](https://developer.android.com/reference/android/Manifest.permission#READ_MEDIA_AUDIO): Allows to read audio files from external storage. Android 13 or higher.
- [`android.permission.READ_MEDIA_VIDEO`](https://developer.android.com/reference/android/Manifest.permission#READ_MEDIA_VIDEO): Allows to read video files from external storage. Android 13 or higher.
- [`android.permission.READ_EXTERNAL_STORAGE`](https://developer.android.com/reference/android/Manifest.permission#READ_EXTERNAL_STORAGE): Allows reading from external storage. Android 12 or lower — bound with `maxSdkVersion` so that it is not requested on Android 13 or higher.

:::danger[Google Play policy]
Google Play's [Photo and Video Permissions policy](https://support.google.com/googleplay/android-developer/answer/14115180)
**rejects** apps targeting Android 13 (API 33) or higher that declare
`READ_MEDIA_IMAGES` or `READ_MEDIA_VIDEO` when the system pickers are sufficient.
Declaring them in *any* active version code — including internal and closed testing
tracks — is enough to block a release.

Use [`FilePicker`](../../services/filepicker.md) unless you genuinely need
library-wide access; in that case you must also submit the photo picker declaration
form in the Play Console.
:::

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-permissions android.permission.READ_MEDIA_AUDIO=true \
  --android-permissions android.permission.READ_MEDIA_VIDEO=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.permission]
"android.permission.READ_MEDIA_AUDIO" = true
"android.permission.READ_MEDIA_VIDEO" = true
"android.permission.READ_EXTERNAL_STORAGE" = { maxSdkVersion = "32" }
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

<CodeExample path={frontMatter.examples + '/video/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/playback/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/screenshot/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/playlist/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/events/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/subtitles/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/controls/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/controls_mode/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/button_bars/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
