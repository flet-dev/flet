---
title: "Packaging app for Linux"
---

Instructions for packaging a Flet app into a Linux executable.

:::tip[Note]
This guide provides detailed Linux-specific information.
Complementary and more general information is available [here](index.md).
:::

## Prerequisites

Flet uses [Flutter](https://flutter.dev) to build Linux apps. Compiling the app
and its native plugins links against GTK and a number of system libraries, so
these must be installed before running `flet build linux`.

On Debian/Ubuntu-based distributions, install the required packages with `apt`:

```bash
sudo apt update
sudo apt install -y \
  binutils clang cmake llvm lld ninja-build pkg-config \
  libgtk-3-dev libsecret-1-0 libsecret-1-dev libunwind-dev \
  gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-libav \
  gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-ugly gstreamer1.0-pulseaudio gstreamer1.0-qt5 \
  gstreamer1.0-tools gstreamer1.0-x \
  libasound2-dev libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev \
  libmpv-dev mpv
```

This is the same set of packages Flet uses in its own build environment. A few
notes on what they are for:

- **Build toolchain** — `clang`, `cmake`, `ninja-build`, `pkg-config`, `llvm`,
  `lld`, `binutils` and `libgtk-3-dev` are required to compile and link the app.
  In particular, the `lld` linker must be present — without it the build fails
  with a linker error.
- **Secret storage** — `libsecret-1-0` and `libsecret-1-dev` are used for secure
  storage / keyring access.
- **Audio and video** — the `gstreamer1.0-*`, `libgstreamer*-dev`,
  `libasound2-dev`, `libmpv-dev` and `mpv` packages are required by the
  [`Audio`](../services/audio/index.md#usage) service and
  [`Video`](../controls/video/index.md#linux) control. You can omit them if your
  app does not play media, but installing the full set above avoids surprises.
  See those pages for control-specific details.

:::note[Other distributions]
Package names differ on non-Debian distributions (e.g. Fedora, Arch). Install
the equivalent GTK 3, GStreamer, `mpv`/`libmpv`, `libsecret`, `clang`/`llvm`,
`lld`, `cmake` and `ninja` development packages for your distribution.
:::

## `flet build linux`

:::note[Note]
This command can be run on **Linux only** (or [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)).
:::

Builds a Linux executable.

## Window positioning on Wayland

On Linux the **display server** controls window placement, and this differs
between X11 and Wayland:

- **X11** lets applications set their own top-level window position.
- **Wayland** (the default session on modern GNOME/Ubuntu) does **not** — by
  design, a client cannot position its own top-level window; the compositor
  (e.g. Mutter) decides where windows are placed.

As a result, on a Wayland session the following have **no effect** (window
*sizing* still works — only positioning is restricted):

- [`Page.window.center()`](../types/window.md)
- setting [`Page.window.left`](../types/window.md) / `Page.window.top`
- moving the window programmatically

This is a Wayland protocol limitation, not a Flet bug. The same code works as
expected on Windows, macOS, Linux X11 sessions, and Wayland sessions running the
app through **XWayland**.

To force the X11 backend (XWayland) on a Wayland session and re-enable
programmatic positioning, run the app with the `GDK_BACKEND` environment
variable:

```bash
GDK_BACKEND=x11 ./your_app
```

You can check the current session type with:

```bash
echo $XDG_SESSION_TYPE   # "wayland" or "x11"
```
