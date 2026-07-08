---
title: "flet build --clear-cache flag deprecated"
---

# `flet build --clear-cache` flag deprecated

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.86.0 deprecated the `--clear-cache` flag of
[`flet build`](../../../cli/flet-build.md) and [`flet debug`](../../../cli/flet-debug.md).

Use the new [`flet clean`](../../../cli/flet-clean.md) command instead.

## Context

`--clear-cache` only deleted the Flutter bootstrap project (`build/flutter`),
and only when the build template hash had changed — so it was a no-op in the
common case and never reset the rest of the `build` directory.

The new [`flet clean`](../../../cli/flet-clean.md) command deletes the entire
`build` directory (the Flutter bootstrap project, cached artifacts, hash stamps,
and generated output) unconditionally, giving a predictable, full reset before
the next build.

## Migration guide

Before:

```bash
flet build web --clear-cache
```

After:

```bash
flet clean
flet build web
```

`flet clean` accepts an optional [path](../../../cli/flet-clean.md#python_app_path) to the app directory (defaults to the
current directory), so you can target another project with `flet clean path/to/app`.

## Timeline

- Deprecated in: `0.86.0`
- Removal in: `0.89.0`

## References

- CLI documentation: [`flet clean`](../../../cli/flet-clean.md), [`flet build`](../../../cli/flet-build.md)
- Issues and PRs: [#6233](https://github.com/flet-dev/flet/issues/6233)
- Release notes: [Flet 0.86.0](../../release-notes.md)
