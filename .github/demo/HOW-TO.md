# Flet Icon Demo — @ARCH@

Two packages of the same app, built by CI from
[flet-dev/flet#2269](https://github.com/flet-dev/flet/issues/2269). Pick
whichever suits you; the AppImage needs no install, the `.deb` shows the
desktop integration properly.

The app should wear a **white "F" on a magenta-to-orange gradient**. Anything
showing the grey Flutter logo instead is the bug this change fixes.

> These are `@ARCH@` builds. Check with `uname -m` — `x86_64` is the `x64`
> artifact, `aarch64` is the `arm64` one. A mismatch only produces
> `Exec format error`.

## AppImage — no install

```bash
chmod +x Flet_Icon_Demo-*.AppImage
./Flet_Icon_Demo-*.AppImage
```

If it exits complaining about FUSE, your distribution has moved to FUSE 3:

```bash
APPIMAGE_EXTRACT_AND_RUN=1 ./Flet_Icon_Demo-*.AppImage
```

An AppImage is not registered with the desktop, so this shows you the window
and dock icon but no app-grid entry.

## .deb — the full desktop integration

```bash
sudo apt install ./@ARTIFACT@_1.0.0_*.deb
```

Then launch it from your app grid, or run `@ARTIFACT@` in a terminal.
Uninstall with `sudo apt remove @ARTIFACT@`.

## What to look at

| Where | What you should see |
| --- | --- |
| Title bar / window list | The demo icon. X11 only — Wayland has no window-icon protocol GTK 3 can reach. |
| Dock / taskbar | The demo icon, while the app is running. |
| App grid (`.deb` only) | An entry named **Flet Icon Demo**, under Graphics. |
| Right-click the dock icon | "Flet Icon Demo", not "flet-icon-demo" or "Flutter". |

On X11 you can read the two properties directly. Run this, then click the app
window when the cursor becomes a crosshair:

```bash
xprop | grep -E "WM_CLASS|_NET_WM_ICON"
```

Expect `WM_CLASS(STRING) = "@BUNDLE_ID@", "@WM_CLASS@"`. GDK capitalises the
second field — that one is the class, the first is the instance, and the
desktop entry's `StartupWMClass` matches the instance. Expect `_NET_WM_ICON`
to begin `256, 256`; before this change there was no window-icon code at all,
so the property was simply absent.

The `256` is also the fix working twice over: an icon larger than GDK's
property size cap is dropped silently rather than truncated, so the runner
scales anything bigger down to 256x256 before handing it over. That is what
would otherwise happen to the 1024x1024 icon `flet build` uses by default.

## Also in this artifact

| File | What it is |
| --- | --- |
| `build-appimage.sh`, `build-deb.sh` | The packaging recipes CI ran, extracted from `website/docs/publish/linux.md` with only the variables the docs tell you to edit. |
| `@BUNDLE_ID@.desktop` | The desktop entry `flet build linux` generated, before packaging rewrote its `Exec=`. |
| `build.log` | The full `flet build linux --verbose` output. |
