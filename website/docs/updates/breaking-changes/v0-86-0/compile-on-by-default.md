---
title: "App and packages are compiled to .pyc by default"
---

# App and packages are compiled to `.pyc` by default

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

`flet build` now **compile your app and the installed
packages to `.pyc` by default** (via `python -m compileall -b`, with the original
`.py` files removed from the bundle). Previously compilation was off unless you
opted in with `--compile-app` / `--compile-packages` or
`[tool.flet.compile]` in `pyproject.toml`.

Shipping bytecode removes per-launch recompilation. The win is largest on
**mobile**, where pure Python is imported from a stored, in-place zip
(`zipimport`) that cannot cache bytecode back to disk — so without precompiled
`.pyc`, every module is recompiled from source on **every** cold start. On a
mid-range Android device this costs roughly 1–2 seconds of startup, scaling with
the number of modules imported.

## Background

Compilation has always been available behind the `--compile-app` /
`--compile-packages` flags; it just defaulted off. With the move to in-place
`zipimport` packaging on Android, leaving it off meant a recurring cold-start tax
on every launch, so the default was flipped on.

Compiled web builds were verified to load correctly in Pyodide: the standalone
CPython used to compile and the Pyodide runtime share the same minor version
(e.g. 3.14), and CPython keeps the `.pyc` magic number stable across patch
releases of a minor version, so the bytecode is accepted.

## Migration guide

Most apps need no changes — builds simply start faster.

If you relied on uncompiled builds (to keep `.py` source in the bundle for
debugging, to let a build complete despite syntax errors, or to speed up
iterative builds), opt out explicitly.

### Opt out via the CLI flag

The flags are now `argparse.BooleanOptionalAction`, so each gets a `--no-` form
(the original `--compile-app` / `--compile-packages` still work):

```bash
flet build apk --no-compile-app --no-compile-packages
```

### Opt out in `pyproject.toml`

```toml
[tool.flet.compile]
app = false
packages = false
```

Per-platform overrides also work, e.g. `[tool.flet.android.compile]`. The
resolution order is CLI flag → `[tool.flet.<platform>.compile]` →
`[tool.flet.compile]` → default (`true`).

## Timeline

- Changed in: `0.86.0`

## References

- API documentation: [Compilation and cleanup](/docs/publish#compilation-and-cleanup)
- Issues and PRs: [#6598](https://github.com/flet-dev/flet/pull/6598)
- Release notes: [Flet 0.86.0](../../release-notes.md)
