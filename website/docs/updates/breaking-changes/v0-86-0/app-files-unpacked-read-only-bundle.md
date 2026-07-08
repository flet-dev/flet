---
title: "App files ship unpacked in a read-only bundle; storage dirs reworked"
---

# App files ship unpacked in a read-only bundle; storage dirs reworked

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.86.0 (with `serious_python` 4.0.0) changes how a packaged app's Python files are shipped and
where the app reads and writes data:

- **App files ship unpacked inside the app bundle**, next to the Python standard library and
  site-packages, on macOS / iOS / Windows / Linux. There is no first-launch `app.zip` extraction. On
  **Android** the app ships as a *stored* `app.zip` asset inside the APK and is unpacked once
  (version-keyed) to the app's files directory on the first launch after an install/update. Web
  (Pyodide) is unchanged.
- The app directory is now **read-only** (signed `.app`, iOS bundle, `Program Files`, the APK).
- The Python program's **current working directory** moved from the app directory to a writable,
  app-private data directory, exposed as `FLET_APP_STORAGE_DATA`.
- `FLET_APP_STORAGE_DATA` now maps to the OS *application support* directory (a `data` subdir),
  **not** the user's Documents folder.
- The storage env vars are now a clean three-tier set: `FLET_APP_STORAGE_DATA` (durable),
  the new **`FLET_APP_STORAGE_CACHE`** (regenerable), and `FLET_APP_STORAGE_TEMP` (now the OS temp
  dir, previously the cache dir).
- `flet run` (dev mode) now sets the working directory to a hidden, git-ignored
  `<project>/.flet/storage/data`, mirroring a built app.

## Background

Previously your Python sources were zipped into `app/app.zip`, shipped as a Flutter asset, and
extracted at runtime on first launch — while the stdlib and site-packages already shipped unpacked
inside the bundle. Lifting app-file handling into `serious_python` removes the first-launch unzip and
the hash bookkeeping, and puts your code in the same place as the stdlib. Because that place is
read-only, the working directory has to move somewhere writable — and the natural home for app data
is the OS *application support* directory, which is app-private on every platform (no Documents
clutter, no manual scoping).

## Migration guide

### Write data to the storage dirs, not next to your code

The app directory is read-only. Relative writes resolve against the **current working directory**,
which is now `FLET_APP_STORAGE_DATA` (a writable, durable, app-private dir). `open("app.db", "w")` and
`sqlite3.connect("app.db")` keep working — the file just lands in the data dir instead of next to your
`.py` files, and now persists across app updates.

### Read shipped files via `__file__`, not relative paths

Relative **reads** of files you bundle with your app (e.g. `open("seed.json")`) no longer resolve
against your app folder. Read bundled data relative to your module instead:

```python
from pathlib import Path

SEED = Path(__file__).parent / "seed.json"
data = SEED.read_text()
```

or use `importlib.resources`, or place the file under your Flet `assets/` directory and resolve it via
`FLET_ASSETS_DIR`.

### Storage environment variables

| Variable | Meaning | Lifetime |
| --- | --- | --- |
| `FLET_APP_STORAGE_DATA` | Durable app data (= the working directory) | Never auto-deleted; backed up |
| `FLET_APP_STORAGE_CACHE` | Regenerable cache (**new**) | OS may purge under storage pressure |
| `FLET_APP_STORAGE_TEMP` | OS temp / scratch (**changed** — was the cache dir) | Most volatile; may vanish between launches |

If you relied on `FLET_APP_STORAGE_TEMP` for data that should survive (it used to be the cache dir),
switch to `FLET_APP_STORAGE_CACHE` (or `FLET_APP_STORAGE_DATA` for must-keep data).

### Physical locations

`FLET_APP_STORAGE_DATA` (= the working directory):

| Platform | Location |
| --- | --- |
| Windows | `%APPDATA%\<company>\<product>\data` (e.g. `C:\Users\<User>\AppData\Roaming\<company>\<product>\data`) |
| macOS | `~/Library/Application Support/<bundle-id>/data` (sandboxed apps: redirected into the app container) |
| Linux | `${XDG_DATA_HOME:-~/.local/share}/<app-id>/data` |
| iOS | `<app-sandbox>/Library/Application Support/<bundle-id>/data` |
| Android | `/data/data/<package>/files/data` |
| `flet run` (dev) | `<project>/.flet/storage/data` |

`FLET_APP_STORAGE_CACHE` and `FLET_APP_STORAGE_TEMP`:

| Platform | `FLET_APP_STORAGE_CACHE` | `FLET_APP_STORAGE_TEMP` |
| --- | --- | --- |
| Windows | `%LOCALAPPDATA%\<company>\<product>` | `%TEMP%` (`…\AppData\Local\Temp`) |
| macOS | `~/Library/Caches/<bundle-id>` | `$TMPDIR` (e.g. `/var/folders/.../T/`) |
| Linux | `${XDG_CACHE_HOME:-~/.cache}/<app-id>` | system temp (`$TMPDIR`, fallback `/tmp`) |
| iOS | `<app-sandbox>/Library/Caches/<bundle-id>` | `<app-sandbox>/tmp` |
| Android | `getCacheDir()` (`/data/data/<package>/cache`) | same as `CACHE` (`getCacheDir()`) |
| `flet run` (dev) | `<project>/.flet/storage/cache` | `<project>/.flet/storage/temp` |

### `flet run` dev storage

`flet run` now creates a hidden `<project>/.flet/` directory (with `storage/{data,cache,temp}`) and
runs your app with the working directory set to `.flet/storage/data`, so dev behaves like a built app
(including the read-shipped-files change above). The directory writes its own `.gitignore` and is
ignored by Git automatically; the old visible `storage/` directory is no longer used.

## Timeline

- Changed in: `0.86.0`

## References

- Environment variables: [`FLET_APP_STORAGE_DATA`](../../../reference/environment-variables.md#flet_app_storage_data),
  [`FLET_APP_STORAGE_CACHE`](../../../reference/environment-variables.md#flet_app_storage_cache),
  [`FLET_APP_STORAGE_TEMP`](../../../reference/environment-variables.md#flet_app_storage_temp)
- Cookbook: [Read and write files](../../../cookbook/read-and-write-files.md)
- Release notes: [Flet 0.86.0](../../release-notes.md)
