---
title: "Linux system libraries"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

On Linux, a Flet app loads some libraries from the system instead of shipping
them, such as GTK, GStreamer, `libmpv` and WebKitGTK. Which ones it needs depends
on the extensions it includes, so they have to be installed on every machine that
runs it.

## What you need to install

| You are | What to install |
|---|---|
| Running an app with `flet run`, or an app made with [`flet pack`](../publish/using-pyinstaller.md), on the default **light** desktop client | `libgtk-3-0` and `libsecret-1-0`, which desktop installations normally include. |
| Running an app on the **full** desktop client | The runtime packages of every extension the full client includes, even ones your app doesn't use. See [Full desktop client](#full-desktop-client). |
| Building an app with [`flet build linux`](../publish/linux.md) | The [build prerequisites](../publish/linux.md#prerequisites), plus the build packages of the extensions your app uses that they leave out (see the table below). |
| Shipping an app built with `flet build linux` | Nothing on your side: your users need the runtime packages of the extensions your app uses. Declare them in your `.deb` or `.rpm` (see [Distributing](../publish/linux.md#distributing)) so the package manager installs them. |

## Libraries by extension

| Extension | Desktop client flavor | Runtime package (Debian, Ubuntu) | Build package (Debian, Ubuntu) | Oldest distribution |
|---|---|---|---|---|
| Every Flet app | light, full | `libgtk-3-0` | `libgtk-3-dev` and the rest of the [build prerequisites](../publish/linux.md#prerequisites) | Every supported one |
| [`flet-secure-storage`](../services/securestorage/index.md) | light, full | `libsecret-1-0` | `libsecret-1-dev` | Every supported one |
| [`flet-audio`](../services/audio/index.md) | full | `libgstreamer-plugins-base1.0-0`, and the GStreamer plugins for the formats you play, such as `gstreamer1.0-plugins-good` | `libgstreamer1.0-dev`, `libgstreamer-plugins-base1.0-dev` | Every supported one |
| [`flet-video`](../controls/video/index.md) | full | `libmpv2` on Debian 12+ and Ubuntu 24.04+; `libmpv1` on earlier releases | `libmpv-dev` | Every supported one |
| [`flet-webview`](../controls/webview/index.md) | full, on Debian 12+ and Ubuntu 22.04+ | `libwebkit2gtk-4.1-0` | `libwebkit2gtk-4.1-dev` | Debian 12, Ubuntu 22.04 |
| [`flet-rive`](../controls/rive/index.md) | full, on Ubuntu 24.04 x86-64 | None | None | Ubuntu 24.04 |

The build prerequisites already include every build package above except
`libwebkit2gtk-4.1-dev`, which is unavailable before Debian 12 and Ubuntu 22.04.

## Full desktop client

The full client includes every extension marked "full" above, so it does not start
until their runtime packages are installed too, next to the light client's
`libgtk-3-0` and `libsecret-1-0`, even for an app that uses none of them. To use
it, set
[`FLET_DESKTOP_FLAVOR=full`](environment-variables.md#flet_desktop_flavor) or
`desktop_flavor = "full"` under `[tool.flet]` in `pyproject.toml`, and install:

<Tabs groupId="linux-distro">
<TabItem value="debian12" label="Debian 12+, Ubuntu 24.04+">

Also Raspberry Pi OS (Bookworm):

```bash
sudo apt install libmpv2 libgstreamer-plugins-base1.0-0 libwebkit2gtk-4.1-0
```
</TabItem>
<TabItem value="ubuntu2204" label="Ubuntu 22.04">

```bash
sudo apt install libmpv1 libgstreamer-plugins-base1.0-0 libwebkit2gtk-4.1-0
```
</TabItem>
<TabItem value="debian11" label="Debian 11, Ubuntu 20.04">

The full client has no `WebView` on these releases:

```bash
sudo apt install libmpv1 libgstreamer-plugins-base1.0-0
```
</TabItem>
<TabItem value="fedora" label="Fedora">

```bash
sudo dnf install mpv-libs gstreamer1-plugins-base webkit2gtk4.1
```
</TabItem>
<TabItem value="opensuse" label="openSUSE Tumbleweed">

```bash
sudo zypper install libmpv2 libgstapp-1_0-0 libwebkit2gtk-4_1-0
```
</TabItem>
<TabItem value="rhel" label="Rocky Linux, AlmaLinux 9">

With EPEL and CRB enabled:

```bash
sudo dnf install mpv-libs gstreamer1-plugins-base
```

These releases have glibc 2.34. The compatible prebuilt full client expects
`libmpv.so.1`, while their repositories ship `libmpv.so.2`. To use audio or video,
build your app with [`flet build linux`](../publish/linux.md#prerequisites)
against the installed libraries. Setting
[`FLET_LINUX_DISTRO=debian12`](environment-variables.md#flet_linux_distro) does
not resolve this mismatch: that build requires glibc 2.36 and cannot run on these
systems.

`WebView` isn't available on these releases: they have no WebKitGTK 4.1.
</TabItem>
</Tabs>

Flet downloads the client build that matches your system's glibc version. On the
Debian, Ubuntu, Fedora and openSUSE releases above, that build expects the `libmpv`
version the distribution ships, so no `libmpv.so.1` symlink is needed. If you created
one for an older Flet version, remove it.

## When a library is missing

A missing library stops an app built with `flet build linux` before any of its
code runs: no window opens, and the app exits with status 127. Run from a
terminal, it prints the library the system could not find:

```
error while loading shared libraries: libwebkit2gtk-4.1.so.0: cannot open shared object file: No such file or directory
```

Started from the application launcher, it shows nothing at all. The app cannot
catch this itself, so make sure the libraries are installed before it runs:
declare them as dependencies of your `.deb` or `.rpm`, and list them for users of
other formats, such as an AppImage or a tarball.

With `flet run` and `flet pack`, the same happens to the desktop client, so your
app's `main()` never runs. Flet then prints the loader error and a hint naming
the packages the client needs.
