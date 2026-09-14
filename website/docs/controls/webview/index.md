---
class_name: "flet_webview.WebView"
examples: "extensions/web_view"
title: "WebView"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

Display web content in a WebView to be shown in your [Flet](https://flet.dev) apps.

It is powered by the [webview_flutter](https://pub.dev/packages/webview_flutter)
and [webview_flutter_web](https://pub.dev/packages/webview_flutter_web) Flutter packages
on Android, iOS, macOS and web, and by
[webview_all_windows](https://pub.dev/packages/webview_all_windows) and
[webview_all_linux](https://pub.dev/packages/webview_all_linux) on Windows and Linux.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

:::note Platform prerequisites
- **Linux** requires `libwebkit2gtk-4.1-0`, available from Debian 12 and Ubuntu 22.04 onward.
  The prebuilt `light` desktop client does not bundle the WebView — use the `full` flavor.
- **Windows** requires the Edge WebView2 runtime, which ships with Windows 11 and is present on
  most, but not all, Windows 10 (1809+) installations.
:::

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
