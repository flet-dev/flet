---
title: "Default bundled Python version is now 3.14"
---

# Default bundled Python version is now 3.14

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.86.0 introduces multi-version bundled CPython support to `flet build`
and `flet publish`. The bundled Python interpreter is now selected per build
(see [Choosing a Python version](/docs/publish#choosing-a-python-version)) and
the **default is the latest supported stable** — currently CPython 3.14.
Earlier Flet releases implicitly bundled CPython 3.12 via the single-version
`serious_python` 1.x.

Apps that depend on Python packages whose pre-built wheels aren't yet
available for 3.14 (typically packages with C/Rust extensions that haven't
caught up to the new ABI) need to pin a previous Python version.

## Background

Multi-version Python support landed in
[#6577](https://github.com/flet-dev/flet/pull/6577) and is tracked by the
central registry in
[`flet_cli/utils/python_versions.py`](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-cli/src/flet_cli/utils/python_versions.py).
The supported short versions are `3.12`, `3.13`, and `3.14` (each pinned to a
specific CPython patch + Pyodide release on the registry side).

The default flips to the latest stable so new projects get the most recent
Python by default. Existing projects without a pin start picking it up too on
their next build.

## Migration guide

You can pin a different Python version in three equivalent ways. Use whichever
fits your project layout.

### Pin in `pyproject.toml` (recommended)

Add or update `[project].requires-python`:

```toml
[project]
requires-python = ">=3.12,<3.13"
```

`flet build` parses the specifier and picks the **highest supported short
version** that satisfies it. So `>=3.12,<3.13` resolves to 3.12,
`>=3.13,<3.14` resolves to 3.13, and `>=3.14` resolves to 3.14 (the default).

### Pin via the CLI flag

Pass `--python-version` on every invocation:

```bash
flet build apk --python-version 3.12
flet publish --python-version 3.12
```

The CLI flag overrides anything in `pyproject.toml`.

### Pin via environment variable

Export `SERIOUS_PYTHON_VERSION` in the shell that runs `flet build`:

```bash
export SERIOUS_PYTHON_VERSION=3.12
flet build apk
```

Useful in CI pipelines where you don't want to thread the flag through every
job.

## Timeline

- Changed in: `0.86.0`

## References

- API documentation: [Choosing a Python version](/docs/publish#choosing-a-python-version)
- Issues and PRs: [#6577](https://github.com/flet-dev/flet/pull/6577)
- Release notes: [Flet 0.86.0](../../release-notes.md)
