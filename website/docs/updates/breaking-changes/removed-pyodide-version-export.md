---
title: "flet.version.pyodide_version and PYODIDE_VERSION removed"
---

# `flet.version.pyodide_version` and `PYODIDE_VERSION` removed

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](.) lists the guides created for each release.
:::

## Summary

Flet 0.86.0 removed the module-level `flet.version.pyodide_version` attribute
and the matching `PYODIDE_VERSION` constant. The single fixed-string export no
longer makes sense now that Pyodide is selected **per build** as part of the
multi-version bundled Python support — the bundled release depends on which
Python version your app pins, not a global default.

## Background

Earlier Flet releases used a single Pyodide pin in `flet.version` to drive the
`flet --version` output and let tooling read which Pyodide release `flet build
web` would bundle. With
[multi-version Python support](/docs/publish#choosing-a-python-version) the
mapping is now Python-version-aware (`3.12 → 0.27.7`, `3.13 → 0.29.4`,
`3.14 → 314.0.0`) and lives in
[`flet_cli/utils/python_versions.py`](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-cli/src/flet_cli/utils/python_versions.py).

`flet --version` now lists every supported Python version with its matching
Pyodide release, newest first.

## Migration guide

If you imported the constant somewhere — typically from `flet.version` —
switch to looking the release up from the new registry.

Code before migration:

```python
import flet.version

print(f"Bundled Pyodide: {flet.version.pyodide_version}")
```

Code after migration:

```python
from flet_cli.utils.python_versions import SUPPORTED_PYTHON_VERSIONS

for release in SUPPORTED_PYTHON_VERSIONS:
    print(f"  {release.short} → Pyodide {release.pyodide}")
```

If you only need the version that `flet build` is about to bundle, resolve
the Python release the same way the CLI does:

```python
from flet_cli.utils.python_versions import (
    DEFAULT_PYTHON_VERSION,
    get_release,
)

release = get_release(DEFAULT_PYTHON_VERSION)
print(f"Default Pyodide: {release.pyodide}")
```

## Timeline

- Removed in: `0.86.0`

## References

- API documentation: [Choosing a Python version](/docs/publish#choosing-a-python-version)
- Issues and PRs: [#6577](https://github.com/flet-dev/flet/pull/6577)
- Release notes: [Flet 0.86.0](../release-notes.md)
