---
class_name: flet_permission_handler.PermissionHandler
examples: ../../examples/controls/permission_handler
---

# Permission Handler

Manage runtime permissions in your [Flet](https://flet.dev) apps using the `flet-permission-handler` extension, powered by Flutter's [`permission_handler`](https://pub.dev/packages/permission_handler).

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ❌     | ❌     | ✅   | ✅       | ✅   |

## Usage

Add `flet-permission-handler` to your project dependencies:

/// tab | uv
```bash
uv add flet-permission-handler
```

///
/// tab | pip
```bash
pip install flet-permission-handler  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Note
    type: note
On mobile platforms you must also declare permissions in the native project files. See [Flet publish docs](https://flet.dev/docs/publish#permissions).
///

## Example

### Example 1

{{ code_and_demo(examples + "/example_1.py", demo_height="420", demo_width="80%") }}

## Description

{{ class_all_options(class_name) }}
