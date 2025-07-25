---
title: Packaging app for Linux
---

Instructions for packaging a Flet app into a Linux executable.

**See complementary information [here](index.md).**

## Prerequisites

### GStreamer for `Audio`

[GStreamer](https://gstreamer.freedesktop.org/) libraries must be installed if your Flet app uses `Audio` control.

To install minimal set of GStreamer libs on Ubuntu/Debian run the following commands:

```
apt install libgtk-3-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

To install full set of GStreamer libs:

```
apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

See [this guide](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c) for installing on other Linux distributives.

### MPV for `Video`

[libmpv](https://mpv.io/) libraries must be installed if your Flet app uses `Video` control.
On Ubuntu/Debian you can install it with:

```
sudo apt install libmpv-dev mpv
```

To build your Flet app that uses `Video` control add `--include-packages flet_video` to `flet build` command, for example:

```
flet build apk --include-packages flet_video
```

## <code class="doc-symbol doc-symbol-command"></code> `flet build linux`

/// admonition | Note
This command can be run on a **Linux only** (or [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)).
///

Builds a Linux executable.
