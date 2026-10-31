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

On Linux, `Video` is only available in the **full** desktop client. The default
**light** client doesn't include it and shows `Unknown control: Video` instead -
set [`FLET_DESKTOP_FLAVOR=full`](../../reference/environment-variables.md#flet_desktop_flavor) or `desktop_flavor = "full"` in `pyproject.toml`,
as described in [Installation](../../getting-started/installation.md#linux).

The full client links against [`libmpv`](https://github.com/mpv-player/mpv) and
GStreamer, so it doesn't start without them
(`error while loading shared libraries: libmpv.so.2` or `libgstapp-1.0.so.0`).
Install the runtime packages.

Debian 12 and later, Ubuntu 24.04 and later, Raspberry Pi OS (Bookworm):

```bash
sudo apt install libmpv2 libgstreamer-plugins-base1.0-0
```

Debian 11, Ubuntu 20.04 and 22.04:

```bash
sudo apt install libmpv1 libgstreamer-plugins-base1.0-0
```

Fedora:

```bash
sudo dnf install mpv-libs gstreamer1-plugins-base
```

openSUSE Tumbleweed:

```bash
sudo zypper install libmpv2 libgstapp-1_0-0
```

Rocky Linux and AlmaLinux 9 (EPEL and RPM Fusion enabled):

```bash
sudo dnf install mpv-libs gstreamer1-plugins-base
export FLET_LINUX_DISTRO=debian12
```

On Rocky Linux and AlmaLinux 9, the build Flet picks for their glibc expects `libmpv.so.1`,
while these repositories ship `libmpv.so.2`, hence
[`FLET_LINUX_DISTRO`](../../reference/environment-variables.md#flet_linux_distro).
On the other distributions above, the client build Flet downloads expects the
`libmpv` version the distribution ships, so no `libmpv.so.1` symlink is needed.
If you created one for an older Flet version, remove it.

[`flet build linux`](../../publish/linux.md#prerequisites) also needs the development
packages, such as `libmpv-dev`, on the build machine.

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
