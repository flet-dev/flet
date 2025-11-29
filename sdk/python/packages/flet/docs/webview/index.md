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

{{ code_and_demo(examples + "/example_1.py", demo_height="420", demo_width="80%") }}

## Description

{{ class_all_options(class_name) }}

See also types:
- [`RequestMethod`](types/request_method.md)
- [`LogLevelSeverity`](types/log_level_severity.md)
- [`WebViewConsoleMessageEvent`](types/webview_console_message_event.md)
- [`WebViewJavaScriptEvent`](types/webview_javascript_event.md)
- [`WebViewScrollEvent`](types/webview_scroll_event.md)
