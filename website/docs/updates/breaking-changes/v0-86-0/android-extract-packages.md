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
`keepDebugSymbols` workarounds. Importing from a zip is transparent to most packages.

Some packages still locate bundled data files through a real filesystem path, usually with
`__file__` or `pkg_resources`, instead of the zip-safe
[`importlib.resources`](https://docs.python.org/3/library/importlib.resources.html). Those packages
must be listed in **`extract_packages`** so they ship extracted to disk.

This affects **Android only**. On macOS, iOS, Windows, and Linux, site-packages ship unpacked;
web (Pyodide) is unchanged.

For the maintained feature documentation, including examples, wildcard behavior, and the current
list of known affected packages, see
[Android packaging: extract packages](../../../publish/android.md#extract-packages).

## Symptoms

The build succeeds, but the app crashes or errors on the device when the package is imported or
first used. The traceback usually contains a path where `sitepackages.zip` or `stdlib.zip` appears
as a directory component, for example:

```bash
FileNotFoundError: [Errno 2] No such file or directory:
  '/data/user/0/<applicationId>/files/.../sitepackages.zip/matplotlib/mpl-data/matplotlibrc'
```

`NotADirectoryError` or `OSError` with a similar `sitepackages.zip/...` path is also a common sign
that the package computed a data path from `__file__` and tried to read it as a regular file.

## Migration guide

Add the failing package's import name to your `pyproject.toml`:

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

Flet extracts the listed package directories and everything under them to the app's files directory,
so `__file__`-relative reads work again.

### No action needed for

- Apps targeting only desktop, iOS, or web.
- Android apps whose dependencies are all zip-safe (the common case) — the change is then purely
  a size win.

## Timeline

- Changed in: `0.86.0`

## References

- [Android packaging: extract packages](../../../publish/android.md#extract-packages)
- [`flet build` CLI reference](../../../cli/flet-build.md)
- Release notes: [Flet 0.86.0](../../release-notes.md)
