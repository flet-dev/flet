---
class_name: flet_flashlight.Flashlight
examples: ../../examples/services/flashlight
---

# Flashlight

Control the device torch/flashlight in your [Flet](https://flet.dev) app via the `flet-flashlight` extension, built on top of Flutter's [`flashlight`](https://pub.dev/packages/flashlight) package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

## Usage

Add `flet-flashlight` to your project dependencies:

/// tab | uv
```bash
uv add flet-flashlight
```

///
/// tab | pip
```bash
pip install flet-flashlight  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
