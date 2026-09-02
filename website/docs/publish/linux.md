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

The [`Categories`](https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html#key-categories)
key of the generated desktop entry determines which menu sections the app
appears under. Values come from the
[freedesktop category registry](https://specifications.freedesktop.org/menu/latest/category-registry.html),
which splits them in two:

- **Main categories** — the fourteen every desktop environment must support:
  `AudioVideo`, `Audio`, `Video`, `Development`, `Education`, `HealthFitness`,
  `Game`, `Graphics`, `Network`, `Office`, `Science`, `Settings`, `System` and
  `Utility`. Normally give exactly one: the spec allows several, but then "the
  entry may appear more than once in the menu".
- **Additional categories** — finer-grained values such as `TextEditor` or
  `ArcadeGame`, listed alongside a main category to refine placement.

A value outside the registry is not an error, but no menu rule matches it, so
it has no effect on where the app appears.

Its value is determined in the following order of precedence:

1. [`--linux-categories`](../cli/flet-build.md#--linux-categories)
2. `[tool.flet.linux].categories`
3. `Utility`

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build linux --linux-categories Game ArcadeGame
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.linux]
categories = ["Game", "ArcadeGame"]
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

The script below fetches
[appimagetool](https://github.com/AppImage/appimagetool/releases) for you, so
there is nothing to download by hand and no path to keep in step. It picks the
build matching the machine you are on — `uname -m` reports `x86_64` or
`aarch64` — and only downloads when the file is not already there, so it costs
nothing on a rebuild and never touches a copy you placed yourself.

`appimagetool` is itself an AppImage, so running it needs
[FUSE 2](https://docs.appimage.org/user-guide/troubleshooting/fuse.html).
Distributions that have moved to FUSE 3 may not have it, so check before
assuming either way:

```bash
ldconfig -p | grep libfuse.so.2
```

If that prints nothing, either install it (`sudo apt install libfuse2`, or
`libfuse2t64` on Ubuntu 24.04 and later) or skip FUSE entirely, by setting the
variable when you run the script below:

```bash
APPIMAGE_EXTRACT_AND_RUN=1 bash build-appimage.sh
```

The same applies to the AppImage you produce: your users need FUSE 2, or must
run it with the same variable set.

**Save** the below script as `build-appimage.sh` (pasting it straight into a terminal is
fragile, and you will re-run it each time you rebuild), then **edit** the three variables
at the top (`BUNDLE`, `APP` & `ID`), and **run** it with `bash build-appimage.sh`.

```bash
#!/usr/bin/env bash
set -euo pipefail # (1)!

BUNDLE=build/linux # (2)!
APP=my_app # (3)!
ID=com.example.my_app # (4)!

APPDIR=MyApp.AppDir # (5)!
ARCH=$(uname -m) # (6)!
APPIMAGETOOL=$PWD/appimagetool-$ARCH.AppImage # (7)!

if [ ! -e "$APPIMAGETOOL" ]; then # (8)!
  wget -O "$APPIMAGETOOL.part" \
    "https://github.com/AppImage/appimagetool/releases/download/1.9.1/appimagetool-$ARCH.AppImage"
  mv "$APPIMAGETOOL.part" "$APPIMAGETOOL"
fi
chmod +x "$APPIMAGETOOL" # (9)!

test -d "$BUNDLE/share/applications" || { echo "no desktop entry in $BUNDLE"; exit 1; } # (10)!

ICON_SRC=$(find "$BUNDLE/share/icons/hicolor" -type f -name "$ID.png" | head -n1) # (11)!
ICON_SIZE=$(basename "$(dirname "$(dirname "$ICON_SRC")")") # (12)!

rm -rf "$APPDIR" # (13)!
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/$ICON_SIZE/apps"

cp -a "$BUNDLE"/. "$APPDIR/usr/bin/" # (14)!
rm -rf "$APPDIR/usr/bin/share" # (15)!

cp "$BUNDLE/share/applications/$ID.desktop" "$APPDIR/usr/share/applications/" # (16)!
cp "$ICON_SRC" "$APPDIR/usr/share/icons/hicolor/$ICON_SIZE/apps/"

sed -i "s|^Exec=.*|Exec=$APP|" "$APPDIR/usr/share/applications/$ID.desktop" # (17)!

ln -s "usr/share/applications/$ID.desktop" "$APPDIR/$ID.desktop" # (18)!
ln -s "usr/share/icons/hicolor/$ICON_SIZE/apps/$ID.png" "$APPDIR/$ID.png" # (19)!
ln -s "usr/share/icons/hicolor/$ICON_SIZE/apps/$ID.png" "$APPDIR/.DirIcon" # (20)!

printf '#!/bin/sh\nHERE=$(dirname "$(readlink -f "$0")")\nexec "$HERE/usr/bin/%s" "$@"\n' "$APP" > "$APPDIR/AppRun" # (21)!
chmod +x "$APPDIR/AppRun"

VERSION=1.0.0 "$APPIMAGETOOL" --no-appstream "$APPDIR" # (22)!
```
1. Stops at the first failing command. Without it a failed copy leaves a
   half-built AppDir, and the error you finally see is `appimagetool`
   complaining about a missing icon several steps later.
2. **Edit this.** Path to the directory `flet build linux` produced — by
   default `build/linux` inside your project. It holds the executable next
   to `data/`, `lib/`, `python3.x/`, `site-packages/` and `app/`. A
   relative path is resolved from wherever you run the script, so prefer an
   absolute one.
3. **Edit this.** The executable's *filename* inside `BUNDLE` — a name, not
   a path. This is your [artifact name](index.md#artifact-name), which
   defaults to your project name. `ls "$BUNDLE"` will show it.
4. **Edit this.** Your [bundle ID](index.md#bundle-id). It must match what
   the app was built with, because it is also the desktop entry's filename
   and the name the window reports; a mismatch means the icon silently
   never resolves.
5. Path to the staging directory this script creates — an **AppDir**, the
   layout `appimagetool` expects: your app, plus a desktop entry, an icon
   and an `AppRun` launcher at its top level. It is deleted and rebuilt on
   every run, so point it somewhere disposable.
6. `x86_64` or `aarch64` — used only to pick the matching `appimagetool`.
7. Where the tool will live, next to wherever you run this script. Nothing
   to edit — the next block puts it there.
8. Fetches `appimagetool` if it is not already there, pinned to a release
   rather than the rolling `continuous` tag so a rebuild cannot silently
   pick up a different tool. The test is for the file *existing*, so a copy
   you put there yourself — from a mirror, say — is never touched. `wget
   -O` truncates its destination before it connects, so the download goes
   to a `.part` file that is only moved into place once it has finished; a
   failed download leaves nothing behind to be mistaken for a working tool.
9. Outside the block, so it also applies to a copy you placed yourself.
   Downloads land without the execute bit — from `wget`, a browser, or an
   extracted archive — and `appimagetool` cannot run without it.
10. Fails early with a clear message if the bundle predates desktop entry
    support, rather than failing obscurely further down.
11. The icon `flet build` installed. Its directory encodes the size, which
    the next line reads, so the AppDir mirrors whatever size your icon is.
12. The size read out of the icon path found on the previous line —
    `256x256` in `.../hicolor/256x256/apps/<id>.png` — so the AppDir
    mirrors whatever size your icon actually is, rather than assuming one.
13. Start from scratch, so a rename or size change cannot leave stale files
    behind.
14. The entire bundle, verbatim. `-a` preserves the executable bit and
    symlinks; the app resolves its libraries and Python runtime relative to
    its own location, so these files must stay together.
15. Removes the `share/` that travelled inside the bundle: the next lines
    put those same two files where AppImage expects them instead, and
    keeping both would ship the desktop entry twice.
16. Places the desktop entry and icon at the paths a Linux system normally
    keeps them. If a user later installs the AppImage into their menus, the
    integration step copies icons out of `usr/share/icons`.
17. A bare name is enough here: inside an AppImage the entry never launches
    the app — the runtime executes `AppRun`. Edit the real file, not the
    symlink created next; GNU `sed -i` would replace a symlink with a
    regular file.
18. AppImage requires exactly one `.desktop` at the AppDir root, and
    `appimagetool` aborts without it.
19. The icon named by the entry's `Icon=` key, at the root. `appimagetool`
    checks for it by that exact name.
20. `.DirIcon` is the AppImage's own icon — the image a file manager shows
    for the `.AppImage` file itself.
21. `AppRun` is the entry point the runtime executes. It only has to `exec`
    the binary — no `cd`, and deliberately no `LD_LIBRARY_PATH`.
22. `VERSION` becomes part of the output filename. `--no-appstream` skips
    AppStream metadata validation, which a minimal app does not ship. Note
    that `appimagetool` downloads the AppImage runtime it embeds, so this
    line needs network even when the tool itself is already on disk; pass
    `--runtime-file` with a locally saved runtime if your build machine has
    none.

:::warning[Do not set `LD_LIBRARY_PATH` in `AppRun`]
Many `AppRun` examples export it. `LD_LIBRARY_PATH` takes precedence over the
binary's `RUNPATH`, so setting it lets system libraries shadow the bundled
ones. The bundle needs no environment at all — `$ORIGIN` resolves against the
executable's own path, so `AppRun` only has to `exec` it.
:::

`appimagetool` requires a `Categories=` key in the desktop entry and runs
`desktop-file-validate` over it, failing on any error. Both are satisfied by
the generated entry.

:::note[An AppImage registers nothing with the desktop]
The desktop entry travels *inside* the image, where nothing scans it. So the
app grid has no entry for the app, and hovering its icon shows the app id
rather than the name — the shell has no `Name=` to read and falls back to what
the window calls itself.

The window and dock icons still work on X11, because those come from the
window's own `_NET_WM_ICON` rather than from an entry. On Wayland, where the
icon is resolved through the entry too, an unregistered AppImage gets neither.

Users can register it themselves with a tool like
[AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher). If you
would rather not ask them to, ship a `.deb` or `.rpm` as well — those install
the entry as part of the package.
:::

</TabItem>
<TabItem value="deb" label=".deb">

Save this as `build-deb.sh`, edit the five variables at the top (`BUNDLE`,
`PKG`, `BIN`, `APPID` and `VER`), and run it with `bash build-deb.sh` on a
machine that has
`dpkg-deb` — that means Linux, not WSL-less Windows or macOS.

```bash
#!/usr/bin/env bash
set -euo pipefail # (1)!

BUNDLE=build/linux # (2)!
PKG=my-app # (3)!
BIN=my-app # (4)!
APPID=com.example.my_app # (5)!
VER=1.0.0 # (6)!

ARCH=$(dpkg --print-architecture) # (7)!
STAGE="build/deb/${PKG}_${VER}_${ARCH}" # (8)!

rm -rf "$STAGE" # (9)!
install -d "$STAGE/DEBIAN" "$STAGE/opt/$PKG" "$STAGE/usr/bin" "$STAGE/usr/share"

cp -a "$BUNDLE"/. "$STAGE/opt/$PKG/" # (10)!

cp -a "$STAGE/opt/$PKG/share/." "$STAGE/usr/share/" # (11)!
rm -rf "$STAGE/opt/$PKG/share" # (12)!

sed -i "s|^Exec=.*|Exec=/opt/$PKG/$BIN %U|" "$STAGE/usr/share/applications/$APPID.desktop" # (13)!

ln -sfn "/opt/$PKG/$BIN" "$STAGE/usr/bin/$PKG" # (14)!

cat > "$STAGE/DEBIAN/control" <<EOF # (15)!
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
chmod 0755 "$STAGE/DEBIAN/postinst" # (16)!

dpkg-deb --build --root-owner-group "$STAGE" "build/${PKG}_${VER}_${ARCH}.deb" # (17)!
```

1. Stops at the first failing command, so a failed copy cannot produce a
   package that installs and then does not run.
2. **Edit this.** Path to the directory `flet build linux` produced — by
   default `build/linux` inside your project.
3. **Edit this.** The Debian package name — lowercase letters, digits and
   `+ - .` only. It is what users type after `apt install`, and the directory
   name under `/opt`.
4. **Edit this.** The executable's *filename* inside `BUNDLE` — a name, not a
   path. This is your [artifact name](index.md#artifact-name).
5. **Edit this.** Your [bundle ID](index.md#bundle-id), which is also the
   desktop entry's filename inside the bundle.
6. **Edit this.** The package version. Debian compares these when deciding
   whether an upgrade applies, so it must increase between releases.
7. `amd64` or `arm64` — Debian's own architecture names, which differ from
   `uname -m` (`x86_64`/`aarch64`), so ask `dpkg` rather than guessing.
8. Staging tree: a directory laid out exactly like the installed system, which
   `dpkg-deb` turns into a package at the end.
9. Rebuild the staging tree from scratch, then create the four directories the
   package installs into.
10. The bundle goes to `/opt/<pkg>` as one piece. `-a` preserves the executable
    bit and symlinks, and the app resolves its libraries and Python runtime
    relative to its own location, so these files must stay together.
11. Copies the bundle's desktop entry and icon to `/usr/share`, which is where
    the desktop looks for installed applications — nothing under `/opt` is
    scanned.
12. Removes the `/opt` copy afterwards, so the entry is not shipped twice.
13. Points `Exec=` at the real install path. The entry ships with a bare name
    because the bundle is relocatable, and nothing on `PATH` would match it.
14. Puts the app on `PATH`. It must be a **symlink, not a wrapper script**:
    the app locates its Python runtime from the path of the running
    executable, and a wrapper would resolve to `/usr/bin` instead of `/opt`.
    The target is absolute because [Debian Policy
    §10.5](https://www.debian.org/doc/debian-policy/ch-files.html#symbolic-links)
    asks for absolute links between top-level directories — the opposite of
    what the `.rpm` recipe uses, where `rpmlint` prefers relative.
15. The package metadata `dpkg` reads. `Section` and `Priority` affect how
    package managers classify it; neither changes behaviour.
16. Maintainer scripts have to be executable, and `dpkg` refuses the package
    otherwise. `postinst` refreshes the desktop and icon caches so the app
    appears in menus without a re-login.
17. `--root-owner-group` records every file as owned by `root` rather than by
    whoever built the package, which is what `lintian` and users expect.

Check the result before publishing it:

```bash
dpkg -c build/my-app_1.0.0_arm64.deb
sudo apt install ./build/my-app_1.0.0_arm64.deb
my-app
```

:::note[Runtime dependencies, not build ones]
`Depends:` lists the shared libraries the app loads at runtime. These are not
the `-dev` packages from [Prerequisites](#prerequisites), which are only needed
on the machine doing the building. The `a | b` alternatives cover Ubuntu 24.04's
rename of several libraries to `…t64`, so one package works on both. Add
`libmpv2` and the GStreamer runtime packages if your app uses the
[`Audio`](../services/audio/index.md#usage) service or the
[`Video`](../controls/video/index.md#linux) control.
:::

</TabItem>
<TabItem value="rpm" label=".rpm">

The same shape as the `.deb`: the bundle installs to `/opt`, its desktop entry
and icon move to `/usr/share`, and `/usr/bin` gets a symlink.

```bash
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
cp -a build/linux ~/rpmbuild/SOURCES/bundle
```

Save the following as `~/rpmbuild/SPECS/my-app.spec` and build it with
`rpmbuild -bb ~/rpmbuild/SPECS/my-app.spec`:

```spec
%global __os_install_post %{nil} # (1)!
%global debug_package %{nil} # (2)!
AutoReqProv: no # (3)!

Name:      my-app # (4)!
Version:   1.0.0
Release:   1%{?dist}
Summary:   One-line summary of My App
License:   Apache-2.0
BuildArch: x86_64 # (5)!
Requires:  gtk3, glib2, gdk-pixbuf2 # (6)!

%description
A longer description of My App.

%install
mkdir -p %{buildroot}/opt/%{name} %{buildroot}/usr/bin %{buildroot}/usr/share
cp -a %{_sourcedir}/bundle/. %{buildroot}/opt/%{name}/ # (7)!
cp -a %{buildroot}/opt/%{name}/share/. %{buildroot}/usr/share/ # (8)!
rm -rf %{buildroot}/opt/%{name}/share
sed -i "s|^Exec=.*|Exec=/opt/%{name}/my-app %U|" %{buildroot}/usr/share/applications/com.example.my_app.desktop # (9)!
ln -sfn ../../opt/%{name}/my-app %{buildroot}/usr/bin/%{name} # (10)!

%files # (11)!
/opt/%{name}
/usr/bin/%{name}
/usr/share/applications/*
/usr/share/icons/hicolor/*/apps/*
```

1. Disables rpmbuild's post-processing. Left on, it byte-compiles the bundled
   `site-packages` with the *system* Python and rewrites shebangs inside the
   bundle — both of which corrupt an app that ships its own interpreter.
2. Skips generating a debuginfo package, which has nothing useful to extract
   from a prebuilt bundle.
3. Stops rpm scanning the bundled `.so` files to auto-generate dependencies.
   Without it the package would demand libraries it already carries.
4. `Name`, `Version` and `Release` together form the package filename, and rpm
   compares them when deciding whether an upgrade applies.
5. Set to the architecture you built on — `x86_64` or `aarch64`. The bundle
   contains a compiled binary, so it is not portable across architectures.
6. Runtime libraries, under their Fedora/RHEL names — the `.deb` names differ.
7. The bundle in one piece, exactly as in the `.deb`.
8. The desktop entry and icon where the desktop scans for them, then the `/opt`
   copy is removed so nothing ships twice.
9. Rewrites the relocatable `Exec=` to the real install path.
10. A symlink rather than a wrapper, so the running executable's path stays
    inside `/opt` and the app can still find its Python runtime. It is written
    relative — from `/usr/bin` that resolves to the same `/opt` path — because
    both rpm and `rpmlint` flag absolute link targets, which break inside a
    chroot.
11. Everything listed here is packaged; anything created in `%install` but not
    listed makes the build fail, which is rpm's way of catching stray files.

</TabItem>
</Tabs>

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
| `rpmbuild` fails at `%mkbuilddir`, reporting `Bad file descriptor`                                                  | An earlier build left `~/rpmbuild/BUILD/<name>-<version>-build` behind and rpm cannot clear it before rebuilding. The errno is unrelated to the real cause — delete that directory and build again. |
