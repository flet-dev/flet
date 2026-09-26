---
class_name: "flet_webview.WebView"
examples: "extensions/web_view"
title: "WebView"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

Display web content in a WebView to be shown in your [Flet](https://flet.dev) apps.

It is powered by the [webview_all](https://pub.dev/packages/webview_all) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add `flet-webview` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-webview
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-webview  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

## Requirements

### Windows

The [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/)
must be installed on the machine running the app. It ships with Windows 11 and is
present on most Windows 10 installations.

When building an app that uses this control, `flet build windows` downloads NuGet and
the WebView2 SDK from [nuget.org](https://www.nuget.org), so the build machine needs
access to it.

### Linux

`libwebkit2gtk-4.1-0` must be installed on the machine running the app, and
`libwebkit2gtk-4.1-dev` on the machine building it. Both are available from Debian 12
and Ubuntu 22.04 (with current updates) onward:

```bash
sudo apt install libwebkit2gtk-4.1-dev
```

When running an app with `flet run`, select the
[full desktop flavor](../../getting-started/installation.md#linux): the default
light flavor does not include this control.

### Web

The page is shown in an `<iframe>`, and Flet's web server (`flet run --web`,
`flet serve`) sends a `Cross-Origin-Embedder-Policy: require-corp` header. A page
from another origin therefore stays blank unless it allows being embedded and sends
both a `Cross-Origin-Resource-Policy: cross-origin` and a `Cross-Origin-Embedder-Policy`
header, which most sites do not.
JavaScript, the page title, scrolling, console messages and alerts are available
only for same-origin pages and for HTML loaded with `load_html()`.

## Example

<CodeExample path={frontMatter.examples + '/web_view/main.py'} language="python" />

## Troubleshooting

### NET::ERR_CLEARTEXT_NOT_PERMITTED Error

If you run into the NET::ERR_CLEARTEXT_NOT_PERMITTED error in Android,
then the app you’re using is trying to access a web page that wants to
transmit cleartext or unsecured information. Android blocks apps from
doing this in order to avoid compromising user data.

For more details, see [this](https://developer.android.com/privacy-and-security/security-config#CleartextTraffic)
and [this](https://kinsta.com/blog/net-err_cleartext_not_permitted/).

To fix it, your app's configuration
(precisely, the [manifest application attributes](../../publish/android.md#application-attributes))
needs to be modified as follows:

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.manifest_application]
usesCleartextTraffic = "true"
```
</TabItem>
</Tabs>
## Description

<ClassAll name={frontMatter.class_name} />
