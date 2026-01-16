---
class_name: flet_secure_storage.SecureStorage
examples: ../../examples/services/secure_storage
---

# Secure Storage

A service for safely storing sensitive key–value data using the platform’s native secure storage mechanisms—Keychain on iOS/macOS, Windows Credential Manager, libsecret on Linux, and Keystore on Android. Supports reliably saving and retrieving data, with optional events for availability changes. Powered by Flutter's [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add `flet-secure-storage` to your project dependencies:

/// tab | uv
```bash
uv add flet-secure-storage
```

///
/// tab | pip
```bash
pip install flet-secure-storage  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Hosting Rive files
    type: tip
Host `.riv` files locally or load them from a CDN. Use `placeholder` to keep layouts responsive while animations load.
///

## Example

```python
--8<-- "{{ examples }}/basic.py"
```

## Description

{{ class_all_options(class_name) }}
