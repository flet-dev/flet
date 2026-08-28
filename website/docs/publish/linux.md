---
title: "Packaging app for Linux"
---

Instructions for packaging a Flet app into a Linux executable.

:::tip[Note]
This guide provides detailed Linux-specific information.
Complementary and more general information is available [here](index.md).
:::

:::info[Alternative: flet pack]
For a PyInstaller-based way to package desktop apps — without the
build-toolchain prerequisites below — see [`flet pack`](using-pyinstaller.md).
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

## App icon

The app icon is taken from `icon_linux.png` (falling back to `icon.png`, or the
default Flet icon) in the `assets` directory of your Flet app — see
[Icons](index.md#icons). `flet build linux` copies it into the bundle as
`data/app_icon.png`, and the app sets it as its window icon on startup.

How the icon shows up depends on the display server (see
[Window positioning on Wayland](#window-positioning-on-wayland) for checking
the session type):

- **X11** (and XWayland): taskbars and window switchers read the window icon
  directly — it works out of the box, no installation needed.
- **Wayland** (the default session on modern GNOME/Ubuntu): the protocol has no
  window-icon concept. The desktop environment resolves the app's name and icon
  from an installed `.desktop` entry matching the app id, and shows a generic
  icon until one is installed.

For Wayland (and for listing the app in the application launcher on any
session), the bundle ships a ready-to-install desktop entry and icon under
`share/`:

```
share/applications/<bundle_id>.desktop
share/icons/hicolor/<size>/apps/<bundle_id>.png
```

`<size>` matches the icon's own pixel size when the icon theme declares it
(`16x16`, `22x22`, `24x24`, `32x32`, `36x36`, `48x48`, `64x64`, `72x72`,
`96x96`, `128x128`, `192x192`, `256x256`, `512x512`), and is `256x256` for any
other size — desktop environments scale from it either way, though some
packaging linters expect the file to match its directory.

To register the app for the current user, copy them into `~/.local/share` and
point `Exec=` at the absolute path of the executable:

```bash
cp -r share/. ~/.local/share/
sed -i "s|^Exec=.*|Exec=\"$PWD/<executable>\" %U|" ~/.local/share/applications/<bundle_id>.desktop
update-desktop-database ~/.local/share/applications
```

(run from the bundle directory, replacing `<executable>` and `<bundle_id>`; a
system-wide install to `/usr/share` works the same way). Keep the quotes around
`Exec=` — without them a path containing spaces is split into separate
arguments and the launcher fails. Linux packaging tools
(`.deb`/`.rpm`/AppImage builders) can pick up the same two files.

The desktop entry's name comes from `--product` and its comment from
`--description` (or the corresponding `pyproject.toml` settings); the app id is
the [bundle ID](index.md#bundle-id) — `<org_name>.<project_name>` by default.
Until the entry is installed the desktop environment has no name for the app
and falls back to that id, so the dock tooltip reads `com.example.my_app`
rather than your product name; installing the entry fixes the name and the
Wayland icon together, since both are resolved from it.

Its [application categories](#application-categories) decide where the app is
filed in application menus.

## Application categories

The [`Categories`](https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html#key-categories) key of the generated desktop entry
determines which menu sections the app appears under. Values must be taken from
the [freedesktop category registry](https://specifications.freedesktop.org/menu/latest/category-registry.html); desktop environments ignore
unregistered ones.

Its value is determined in the following order of precedence:

1. [`--linux-categories`](../cli/flet-build.md#--linux-categories)
2. `[tool.flet.linux].categories`
3. `Utility`

```bash
flet build linux --linux-categories Game Education
```

```toml
[tool.flet.linux]
categories = ["Game", "Education"]
```

## Window positioning on Wayland

On Linux the **display server** controls window placement, and this differs
between X11 and Wayland:

- **X11** lets applications set their own top-level window position.
- **Wayland** (the default session on modern GNOME/Ubuntu) does **not** — by
  design, a client cannot position its own top-level window; the compositor
  (e.g. Mutter) decides where windows are placed.

As a result, on a Wayland session the following have **no effect** (window
*sizing* still works — only positioning is restricted):

- [`Page.window.center()`][flet.Window.center]
- setting [`Page.window.left`][flet.Window.left] / [`Page.window.top`][flet.Window.top]
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

## Troubleshooting

| Symptom                                                                                                             | Cause and fix                                                                                                                                                                                                                                                     |
|---------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Build fails with a linker error                                                                                     | The `lld` linker is missing — it is part of the [prerequisites](#prerequisites): `sudo apt install lld` (or your distribution's equivalent) and rebuild.                                                                                                          |
| CMake can't find `gtk+-3.0` or other packages                                                                       | One or more `-dev` [prerequisites](#prerequisites) are missing — install the full list (package names differ on non-Debian distributions).                                                                                                                        |
| The built app won't start on users' machines: `error while loading shared libraries: libmpv…` (or GStreamer errors) | The [`Audio`](../services/audio/index.md#usage) service and [`Video`](../controls/video/index.md#linux) control link against system libraries — `mpv`/`libmpv` and GStreamer must also be installed on the machine *running* the app, not only the build machine. |
| Window positioning or centering has no effect                                                                       | The app is running in a Wayland session — see [Window positioning on Wayland](#window-positioning-on-wayland).                                                                                                                                                    |
| The taskbar/dock shows a generic icon on Wayland                                                                    | Wayland resolves icons from an installed desktop entry, not from the window — install the bundle's `share/` files as described in [App icon](#app-icon).                                                                                                          |
| The dock tooltip or app switcher shows the bundle ID instead of the app name                                        | The desktop entry is not installed, so the desktop environment has no name for the app and falls back to the app id — install the bundle's `share/` files as described in [App icon](#app-icon). |
