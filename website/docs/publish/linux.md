---
title: "Packaging app for Linux"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import LinuxDependencies from '@site/.crocodocs/linux-dependencies.mdx';

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

<Tabs groupId="linux-deps">
<TabItem value="packages" label="Package list">
<LinuxDependencies />
</TabItem>
<TabItem value="cli" label="From the CLI">

`flet --version` reports the same list, so a setup script never goes stale:

```bash
sudo apt update
sudo apt install -y $(flet --version --json | jq -r '.linux_dependencies | join(" ")')
```
</TabItem>
<TabItem value="cli-no-jq" label="From the CLI (without jq)">

Same thing where [`jq`](https://jqlang.org) is not installed:

```bash
sudo apt update
sudo apt install -y $(flet --version --json \
  | python3 -c "import json,sys; print(' '.join(json.load(sys.stdin)['linux_dependencies']))")
```
</TabItem>
</Tabs>

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

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build linux --linux-categories Game Education
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.linux]
categories = ["Game", "Education"]
```
</TabItem>
</Tabs>

## Distributing

`flet build linux` leaves a **relocatable bundle directory** — an executable
alongside `data/`, `lib/`, `python3.x/`, `site-packages/` and `app/` — not
something an end user can download and double-click. To ship it, wrap it in one
of the formats below.

Packaging is mostly relocation, because the bundle already contains the two
files every Linux format wants:

```
share/applications/<bundle_id>.desktop
share/icons/hicolor/<size>/apps/<bundle_id>.png
```

Two rules apply to every format:

- **Keep the bundle together.** The executable finds its libraries through
  `RPATH $ORIGIN/lib` and its Python runtime through its own path, so `data/`,
  `lib/`, `python3.x/`, `site-packages/` and `app/` must stay siblings of the
  executable. Do not scatter them into `/usr/bin` and `/usr/lib`.
- **Rewrite `Exec=`.** The shipped entry names the executable without a path,
  since the bundle does not know where it will be installed. Every recipe below
  replaces that line with the real location.

<Tabs groupId="linux-packaging">
<TabItem value="appimage" label="AppImage">

A single executable file that runs without installation — the closest
equivalent to a macOS `.dmg`.

Get the tool for your architecture from
[AppImage/appimagetool](https://github.com/AppImage/appimagetool/releases)
(`appimagetool-x86_64.AppImage` or `appimagetool-aarch64.AppImage`) and make it
executable.

`appimagetool` is itself an AppImage, so running it needs
[FUSE 2](https://docs.appimage.org/user-guide/troubleshooting/fuse.html) —
which Ubuntu 22.04 and later no longer install by default, having moved to
FUSE 3. Check with:

```bash
ldconfig -p | grep libfuse.so.2
```

If that prints nothing, either install it (`sudo apt install libfuse2`, or
`libfuse2t64` on Ubuntu 24.04 and later) or skip FUSE entirely:

```bash
APPIMAGE_EXTRACT_AND_RUN=1 ./appimagetool-x86_64.AppImage --no-appstream MyApp.AppDir
```

The same applies to the AppImage you produce: your users need FUSE 2, or must
run it with the same variable set.

```bash
#!/usr/bin/env bash
set -euo pipefail

BUNDLE=build/linux            # output of `flet build linux`
APP=my_app                    # the executable in $BUNDLE (your artifact name)
ID=com.example.my_app         # your bundle ID
APPDIR=MyApp.AppDir

ICON_SRC=$(find "$BUNDLE/share/icons/hicolor" -type f -name "$ID.png" | head -n1)
ICON_SIZE=$(basename "$(dirname "$(dirname "$ICON_SRC")")")

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" \
         "$APPDIR/usr/share/icons/hicolor/$ICON_SIZE/apps"

# The whole bundle, verbatim — -a preserves modes and symlinks.
cp -a "$BUNDLE"/. "$APPDIR/usr/bin/"
rm -rf "$APPDIR/usr/bin/share"

cp "$BUNDLE/share/applications/$ID.desktop" "$APPDIR/usr/share/applications/"
cp "$ICON_SRC" "$APPDIR/usr/share/icons/hicolor/$ICON_SIZE/apps/"

# Inside an AppImage the entry is not what launches the app, so a bare name
# is enough. Edit the real file, not the symlink created below.
sed -i "s|^Exec=.*|Exec=$APP|" "$APPDIR/usr/share/applications/$ID.desktop"

# AppImage requires all four of these at the AppDir root.
ln -s "usr/share/applications/$ID.desktop"              "$APPDIR/$ID.desktop"
ln -s "usr/share/icons/hicolor/$ICON_SIZE/apps/$ID.png" "$APPDIR/$ID.png"
ln -s "usr/share/icons/hicolor/$ICON_SIZE/apps/$ID.png" "$APPDIR/.DirIcon"

cat > "$APPDIR/AppRun" <<EOF
#!/bin/sh
HERE=\$(dirname "\$(readlink -f "\$0")")
exec "\$HERE/usr/bin/$APP" "\$@"
EOF
chmod +x "$APPDIR/AppRun"

VERSION=1.0.0 ./appimagetool-x86_64.AppImage --no-appstream "$APPDIR"
```

:::warning[Do not set `LD_LIBRARY_PATH` in `AppRun`]
Many `AppRun` examples export it. `LD_LIBRARY_PATH` takes precedence over the
binary's `RUNPATH`, so setting it lets system libraries shadow the bundled
ones. The bundle needs no environment at all — `$ORIGIN` resolves against the
executable's own path, so `AppRun` only has to `exec` it.
:::

`appimagetool` requires a `Categories=` key in the desktop entry and runs
`desktop-file-validate` over it, failing on any error. Both are satisfied by
the generated entry.

</TabItem>
<TabItem value="deb" label=".deb">

```bash
#!/usr/bin/env bash
set -euo pipefail

PKG=my-app                    # package name: lowercase, digits, + - .
BIN=my-app                    # the executable in build/linux
APPID=com.example.my_app      # your bundle ID
VER=1.0.0
ARCH=$(dpkg --print-architecture)
STAGE="build/deb/${PKG}_${VER}_${ARCH}"

rm -rf "$STAGE"
install -d "$STAGE/DEBIAN" "$STAGE/opt/$PKG" "$STAGE/usr/bin" "$STAGE/usr/share"

# The bundle stays intact under /opt.
cp -a build/linux/. "$STAGE/opt/$PKG/"

# Its XDG tree moves to /usr/share, where the desktop looks for it.
cp -a "$STAGE/opt/$PKG/share/." "$STAGE/usr/share/"
rm -rf "$STAGE/opt/$PKG/share"

sed -i "s|^Exec=.*|Exec=/opt/$PKG/$BIN %U|" \
  "$STAGE/usr/share/applications/$APPID.desktop"

# A symlink, not a wrapper script: the app resolves its own path to find its
# Python runtime, so it must be started as /opt/<pkg>/<bin>.
ln -sfn "/opt/$PKG/$BIN" "$STAGE/usr/bin/$PKG"

cat > "$STAGE/DEBIAN/control" <<EOF
Package: $PKG
Version: $VER
Architecture: $ARCH
Maintainer: Your Name <you@example.com>
Section: utils
Priority: optional
Depends: libgtk-3-0 | libgtk-3-0t64, libglib2.0-0 | libglib2.0-0t64, libgdk-pixbuf-2.0-0, libstdc++6, libgcc-s1, libc6
Description: One-line summary of My App
 A longer description, with every line indented by one space.
EOF

cat > "$STAGE/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
if [ "$1" = configure ]; then
  update-desktop-database -q /usr/share/applications 2>/dev/null || true
  gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
fi
EOF
chmod 0755 "$STAGE/DEBIAN/postinst"

dpkg-deb --build --root-owner-group "$STAGE" "build/${PKG}_${VER}_${ARCH}.deb"
```

:::note[Runtime dependencies, not build ones]
`Depends:` lists the shared libraries the app loads at runtime. These are not
the `-dev` packages from [Prerequisites](#prerequisites), which are only needed
on the machine doing the building. Add `libmpv2` and the GStreamer runtime
packages if your app uses the
[`Audio`](../services/audio/index.md#usage) service or the
[`Video`](../controls/video/index.md#linux) control.
:::

</TabItem>
<TabItem value="rpm" label=".rpm">

The same shape as the `.deb`, expressed as a spec file. Copy `build/linux` to
`rpmbuild/SOURCES/bundle`, then:

```spec
# rpmbuild would otherwise byte-compile the bundled site-packages with the
# system Python and rewrite shebangs inside the bundle.
%global __os_install_post %{nil}
%global debug_package     %{nil}
AutoReqProv: no

Name:      my-app
Version:   1.0.0
Release:   1%{?dist}
Summary:   One-line summary of My App
License:   Apache-2.0
Requires:  gtk3, glib2, gdk-pixbuf2

%install
mkdir -p %{buildroot}/opt/%{name} %{buildroot}/usr/bin %{buildroot}/usr/share
cp -a %{_sourcedir}/bundle/. %{buildroot}/opt/%{name}/
cp -a %{buildroot}/opt/%{name}/share/. %{buildroot}/usr/share/
rm -rf %{buildroot}/opt/%{name}/share
sed -i "s|^Exec=.*|Exec=/opt/%{name}/my-app %U|" \
  %{buildroot}/usr/share/applications/com.example.my_app.desktop
ln -sfn /opt/%{name}/my-app %{buildroot}/usr/bin/%{name}

%files
/opt/%{name}
/usr/bin/%{name}
/usr/share/applications/*
/usr/share/icons/hicolor/*/apps/*
```

</TabItem>
</Tabs>

:::info[Why not `fastforge`?]
[`fastforge`](https://pub.dev/packages/fastforge) (formerly
`flutter_distributor`) packages Flutter Linux apps, but it always runs
`flutter build linux` itself before packaging. A Flet app's Python payload is
staged by a separate step and is only installed when `flet build` sets its
environment, so a rebuild driven from outside produces a bundle with no `app/`
or `site-packages/` — one that installs cleanly and then fails to start. It
also writes its own desktop entry rather than reusing the one in the bundle,
which drops the `StartupWMClass` that Wayland needs to match the window to its
icon.
:::

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
