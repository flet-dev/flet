---
title: "Upgrade Flet"
---

# Upgrade Flet

## pip

Upgrade Flet and its standard companion packages:

```bash
pip install 'flet[all]' --upgrade
```

## uv

If your project uses `pyproject.toml`, upgrade everything in the environment:

```bash
uv sync --upgrade
```

To upgrade only Flet packages:

```bash
uv sync --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web
```

## Before upgrading

Check the release you are moving to:

- [Release notes](release-notes.md) for the release summary.
- [Deprecations](deprecations.md) for APIs that are still available but scheduled
  for removal.
- [Breaking changes](breaking-changes/index.md) for required migrations.
