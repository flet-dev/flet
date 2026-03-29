---
class_name: flet_permission_handler.PermissionHandler
examples: ../../examples/services/permission_handler
---

# Permission Handler

Helps manage runtime permissions in your [Flet](https://flet.dev) apps.

It is powered by the Flutter [`permission_handler`](https://pub.dev/packages/permission_handler) package.

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
On mobile platforms you must also declare permissions in the native project files. See [Flet publish docs](../publish/index.md#permissions).
///

## Requirements

While the permissions are being requested during runtime,
you'll still need to tell the OS which permissions your app might potentially use.

### Android

See:

- [full list of Android permissions](https://developer.android.com/reference/android/Manifest.permission)
- [`Permission`][flet_permission_handler.Permission] enum, which lists all the supported permissions
- [setting Android permissions](../publish/android.md#permissions)

### iOS

See:

- [`Permission`][flet_permission_handler.Permission] enum, which lists all the supported permissions and their `Info.plist` keys
- [setting iOS permissions](../publish/ios.md#permissions)

## Example

```python
--8<-- "{{ examples }}/example_1/main.py"
```

## Description

{{ class_all_options(class_name) }}
