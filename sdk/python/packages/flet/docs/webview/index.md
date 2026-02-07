---
class_name: flet_webview.WebView
examples: ../../examples/controls/webview
---

# WebView

Display web content inside your [Flet](https://flet.dev) app using the `flet-webview` extension, which wraps Flutter's [`webview_flutter`](https://pub.dev/packages/webview_flutter) package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ❌       | ✅     | ❌     | ✅   | ✅       | ✅   |

## Usage

Add `flet-webview` to your project dependencies:

/// tab | uv
```bash
uv add flet-webview
```

///
/// tab | pip
```bash
pip install flet-webview  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Troubleshooting

### NET::ERR_CLEARTEXT_NOT_PERMITTED Error

If you run into the NET::ERR_CLEARTEXT_NOT_PERMITTED error in Android,
then the app you’re using is trying to access a web page that wants to
transmit cleartext or unsecured information. Android blocks apps from
doing this in order to avoid compromising user data.

For more details, see [this](https://developer.android.com/privacy-and-security/security-config#CleartextTraffic)
and [this](https://kinsta.com/blog/net-err_cleartext_not_permitted/).

To fix it, the `AndroidManifest.xml` file needs to be modified, to include the `android:usesCleartextTraffic=”true”`.
This can be done through one of the following methods:

/// tab | `pyproject.toml`
```toml
[tool.flet.android.manifest_application]
usesCleartextTraffic = "true"
```
///

## Description

{{ class_all_options(class_name) }}
