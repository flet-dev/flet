---
class_name: flet_rive.Rive
examples: ../../examples/controls/rive
---

# Rive

Render [Rive](https://rive.app/) animations in your [Flet](https://flet.dev) app with the `flet-rive` extension.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅  (x64 only) |  ✅  |    ✅    |  ✅  |

## Usage

Add `flet-rive` to your project dependencies:

/// tab | uv
```bash
uv add flet-rive
```

///
/// tab | pip
```bash
pip install flet-rive  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Hosting Rive files
    type: tip
Host `.riv` files locally or load them from a CDN. Use `placeholder` to keep layouts responsive while animations load.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
