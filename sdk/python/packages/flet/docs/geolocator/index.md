---
class_name: flet_geolocator.Geolocator
examples: ../../examples/controls/geolocator
---

# Geolocator

Access device location services in your [Flet](https://flet.dev) app using the `flet-geolocator` extension. The control wraps Flutter's [`geolocator`](https://pub.dev/packages/geolocator) package and exposes async helpers for permission checks and position streams.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add `flet-geolocator` to your project dependencies:

/// tab | uv
```bash
uv add flet-geolocator
```

///
/// tab | pip
```bash
pip install flet-geolocator  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Important
    type: note
Request permissions with `request_permission` or `get_permission_status` before relying on location data.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
