---
class_name: "flet_webview_all.FletWebviewAll"
examples: "extensions/webview_all"
title: "WebViewAll"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# WebViewAll

Display web content in Flet applications on Windows, macOS, Linux, iOS, Android,
and Web using the [`webview_all`](https://pub.dev/packages/webview_all) Flutter package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Setup

No additional platform configuration is required. Add `flet-webview-all` to your
project dependencies as shown below.

## Usage

Add `flet-webview-all` to the project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">

```bash
uv add flet-webview-all
```

</TabItem>
<TabItem value="pip" label="pip">

```bash
pip install flet-webview-all  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

## Example

<CodeExample path={frontMatter.examples + '/webview_all/main.py'} language="python" />

## Properties

| Property | Type | Description |
|---|---|---|
| `url` | `str \| None` | URL of the page to load. |
| `html` | `str \| None` | HTML content to load instead of a URL. |
| `allow_navigation` | `bool` | Allows or prevents navigation requested by the page. |
| `zoom_enabled` | `bool` | Enables or disables page zooming. |
| `javascript_enabled` | `bool` | Enables or disables JavaScript execution. |
| `javascript_mode` | `str \| bool \| None` | JavaScript mode used by the WebView. |
| `javascript_channels` | `list[str] \| None` | Names of JavaScript channels exposed to the page. |
| `user_agent` | `str \| None` | Custom HTTP `User-Agent` request-header value. |
| `debugging_enabled` | `bool` | Enables WebView debugging. |
| `background_color` | `ColorValue \| None` | Background color of the WebView. |
| `allow_webview_permissions` | `bool` | Allows pages to request protected WebView resources. |
| `remote_debugging_port` | `int \| None` | Port used for remote WebView debugging. |

## Events

Event handlers receive typed event objects:

| Event | Event type | Description |
|---|---|---|
| `on_page_started` | [`WebViewPageEvent`](types/webviewpageevent.md) | Fires when page loading starts. Contains `url`. |
| `on_page_finished` | [`WebViewPageEvent`](types/webviewpageevent.md) | Fires when page loading finishes. Contains `url`. |
| `on_progress` | [`WebViewProgressEvent`](types/webviewprogressevent.md) | Reports loading progress from 0 through 100. |
| `on_web_resource_error` | [`WebViewResourceErrorEvent`](types/webviewresourceerrorevent.md) | Reports a failed resource, including its domain, description, error code, error type, and whether it belongs to the main frame. |
| `on_navigation_request` | [`WebViewNavigationRequestEvent`](types/webviewnavigationrequestevent.md) | Fires when navigation is requested. Contains `url` and `is_main_frame`. |
| `on_javascript_message` | [`WebViewJavaScriptMessageEvent`](types/webviewjavascriptmessageevent.md) | Fires when a registered JavaScript channel receives a message. |
| `on_permission_request` | [`WebViewPermissionRequestEvent`](types/webviewpermissionrequestevent.md) | Fires when a page requests WebView permissions. Contains `resource_types`. |
| `on_scroll_position_change` | [`WebViewScrollEvent`](types/webviewscrollevent.md) | Reports the current scroll position through `x` and `y`. |
| `on_console_message` | [`WebViewConsoleMessageEvent`](types/webviewconsolemessageevent.md) | Reports a JavaScript console message and its `level`. |

## Methods

All methods are asynchronous and must be awaited after the control has been added to a page.

| Method | Description |
|---|---|
| `reload()` | Reloads the current page. |
| `stop_loading()` | Stops loading the current page. |
| `can_go_back()` | Returns whether browser history has a previous entry. |
| `go_back()` | Navigates to the previous history entry, if any. |
| `can_go_forward()` | Returns whether browser history has a following entry. |
| `go_forward()` | Navigates to the next history entry, if any. |
| `clear_cache()` | Clears the browser HTTP, Cache API, and application caches. |
| `clear_cookies()` | Clears cookies shared by WebViews and returns whether the operation succeeded. |
| `get_current_url()` | Returns the URL currently displayed by the WebView. |
| `run_javascript(script)` | Evaluates JavaScript in the active document without returning a value. |
| `run_javascript_returning_result(script)` | Evaluates JavaScript and returns a platform-serializable result. |
| `scroll_to(x, y)` | Scrolls to an absolute document position in pixels. |
| `scroll_by(delta_x, delta_y)` | Scrolls by a relative document offset in pixels. |
| `get_scroll_position()` | Returns the current horizontal and vertical scroll offsets. |
| `supports_set_scrollbars_enabled()` | Returns whether the current engine supports scrollbar visibility controls. |
| `set_vertical_scrollbar_enabled(enabled)` | Shows or hides the vertical scrollbar when supported. |
| `set_horizontal_scrollbar_enabled(enabled)` | Shows or hides the horizontal scrollbar when supported. |
| `open_devtools()` | Opens native WebView developer tools when supported. |
| `get_webview_version()` | Returns the WebView runtime version when available. |

## Description

<ClassAll name={frontMatter.class_name} />
