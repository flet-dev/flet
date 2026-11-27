---
class_name: "flet_audio.Audio"
examples: "extensions/audio"
title: "Audio"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Audio

Allows playing audio in [Flet](https://flet.dev) apps.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

To use `Audio` control add `flet-audio` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-audio
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-audio  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
:::note[Linux requirements]
On Linux, `Audio` is only available in the **full** desktop client. With the default **light**
client, calls such as [`play()`][flet_audio.Audio.play] fail with `Timeout waiting for invoke method listener` - set
[`FLET_DESKTOP_FLAVOR=full`](../../reference/environment-variables.md#flet_desktop_flavor) or `desktop_flavor = "full"` in `pyproject.toml`, as described in
[Installation](../../getting-started/installation.md#linux).

The full client and apps built with `flet build linux` play audio through
[GStreamer](https://gstreamer.freedesktop.org), loaded from the system, and the full
client doesn't start without the libraries of the other extensions it includes either.
See [Linux system libraries](../../reference/linux-system-libraries.md) for the packages
to install, both to run and to build apps. The same applies on
[WSL](https://docs.microsoft.com/en-us/windows/wsl/about).

Each audio format also needs the GStreamer plugin that decodes it, such as
`gstreamer1.0-plugins-good` or `gstreamer1.0-libav`.
:::

## Examples

<CodeExample path={frontMatter.examples + '/audio_playback_controls/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
