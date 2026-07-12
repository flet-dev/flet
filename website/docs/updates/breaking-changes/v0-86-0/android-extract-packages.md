---
title: "Android: site-packages ship zipped; some packages need extract_packages"
---

# Android: site-packages ship zipped; some packages need `extract_packages`

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.86.0 changes how Python code is packaged into Android apps (`flet build apk` / `aab`):

- **Native extension modules** (`.so` files) are loaded **memory-mapped directly from the APK** —
  no extraction to disk.
- **Pure Python code** — the standard library and your site-packages — ships in *stored* zip
  assets (`stdlib.zip`, `sitepackages.zip`) and is imported **in place** via
  [`zipimport`](https://docs.python.org/3/library/zipimport.html), so it is no longer duplicated
  per ABI or unpacked on first launch.

This makes APKs significantly smaller and removes the need for `useLegacyPackaging` /
`keepDebugSymbols` workarounds. Importing from a zip is transparent to most packages — **but
packages that locate their bundled data files through a real filesystem path** (via `__file__`
or `pkg_resources`, instead of the zip-safe
[`importlib.resources`](https://docs.python.org/3/library/importlib.resources.html)) **fail at
runtime on the device**, because their data now lives inside `sitepackages.zip` where plain
`open()` can't reach it.

Such packages must be listed in the new **`extract_packages`** setting so they ship extracted to
disk instead.

This affects **Android only**. On macOS, iOS, Windows, and Linux, site-packages ship unpacked;
web (Pyodide) is unchanged.

## How the problem looks

The build succeeds, but the app crashes or errors on the device when the package is imported or
first used, with a not-very-helpful traceback such as:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '/data/user/0/<applicationId>/files/.../sitepackages.zip/matplotlib/mpl-data/matplotlibrc'
```

or a `NotADirectoryError` / `OSError` with a path containing `sitepackages.zip/`. A path that has
`sitepackages.zip` (or `stdlib.zip`) as one of its *directory* components is the telltale sign:
the package computed a data path from `__file__` and tried to read it as a regular file.

## Migration guide

### List path-hungry packages in `extract_packages`

Add the failing packages to your `pyproject.toml`:

```toml
[tool.flet.android]
extract_packages = ["matplotlib", "sklearn"]
```

or pass them on the command line:

```bash
flet build apk --android-extract-packages matplotlib sklearn
```

An entry is the package's **import name** — its top-level directory under site-packages — not
the PyPI distribution name: `sklearn`, not `scikit-learn`; `cv2`, not `opencv-python`.
(`matplotlib` matches only because its import name happens to equal its PyPI name.)

Listed packages (and everything under their directory) are moved out of `sitepackages.zip` and
shipped extracted to the app's files directory, so `__file__`-relative reads work again.

Resolution order:

1. [`--android-extract-packages`](../../../cli/flet-build.md#--android-extract-packages)
2. `[tool.flet.android].extract_packages`
3. `[tool.flet].extract_packages`

### Wildcards

An entry is a path relative to site-packages and matches that path and everything under it.
Entries may also contain `*` / `?` wildcards, matched against the top-level directory name:

```toml
[tool.flet.android]
extract_packages = ["mypackage*"]
```

also extracts the sibling `mypackage-<version>.dist-info/` directory — use the wildcard form for
packages that read their metadata or data files through `pkg_resources`.

### Which packages need this?

Only packages that read bundled data through a real filesystem path. Most packages that bundle
data read it via `importlib.resources`, which works from inside the zip and needs **no** entry —
for example `certifi.where()` works as is.

Known packages that need an entry (community-reported; the list will grow as more are found):

| package (PyPI) | entry | why |
|---|---|---|
| `matplotlib` | `"matplotlib"` | reads `mpl-data` (fonts, `matplotlibrc`) relative to `__file__` |
| `scikit-learn` | `"sklearn"` | loads bundled data files through `__file__`-relative paths |
| `opencv-python` | `"cv2"` | cv2's bootstrap resolves its config files and loads its native extension through `__file__`-relative paths, so it must ship as a real directory |
| `astropy` | `"astropy"` | reads `astropy/CITATION` via `__file__` at import |
| `thinc` | `"thinc"` | reads `thinc/backends/_custom_kernels.cu` via `__file__` at import |
| `spacy` | `"spacy", "thinc"` | imports thinc at load (so it hits thinc's `_custom_kernels.cu`) and reads its own language data via `__file__` — list both |

If a package of yours fails with a `sitepackages.zip/...` path in the traceback, add it to
`extract_packages` — and consider reporting it in
[Flet discussions](https://github.com/flet-dev/flet/discussions) so it can be added to the list
above.

### No action needed for

- Apps targeting only desktop, iOS, or web.
- Android apps whose dependencies are all zip-safe (the common case) — the change is then purely
  a size win.

## Timeline

- Changed in: `0.86.0`

## References

- [Android packaging: extract packages](../../../publish/android.md#android-extract-packages)
- [`flet build` CLI reference](../../../cli/flet-build.md)
- Release notes: [Flet 0.86.0](../../release-notes.md)
