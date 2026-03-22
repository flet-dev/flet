---
examples: "../../examples/controls/ads"
example_images: "../examples/controls/ads/media"
title: "Ads"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {CodeExample, Image} from '@site/src/components/crocodocs';

# Ads

Displaying Google Ads in [Flet](https://flet.dev) apps.

It is powered by the [google_mobile_ads](https://pub.dev/packages/google_mobile_ads) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ❌       | ❌     | ❌     | ✅   | ✅       | ❌   |

## Usage

To use ads controls add `flet-ads` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-ads
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-ads  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Requirements

The below sections show the required configurations for each platform.

### Android

A valid [AdMob app ID](https://support.google.com/admob/answer/7356431)
is required to be specified, otherwise the app might crash on launch or behave unexpectedly.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-meta-data com.google.android.gms.ads.APPLICATION_ID="ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.meta_data]
"com.google.android.gms.ads.APPLICATION_ID" = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```
</TabItem>
</Tabs>
See also:

- [setting Android permissions](../publish/android.md#permissions)
- [AdMob app ID for testing purposes](#test-values)

### iOS

A valid [AdMob app ID](https://support.google.com/admob/answer/7356431)
is required to be specified, otherwise the app might crash on launch or behave unexpectedly.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build ipa \
  --info-plist GADApplicationIdentifier="ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.ios.info]
GADApplicationIdentifier = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```
</TabItem>
</Tabs>
See also:

- [setting iOS permissions](../publish/ios.md#permissions)
- [AdMob app ID for testing purposes](#test-values)

### Test Values

AdMob [provides](https://developers.google.com/admob/flutter/banner#always_test_with_test_ads) app and ad unit IDs for
testing purposes.

* **AdMob app ID**: `"ca-app-pub-3940256099942544~3347511713"`
* [`BannerAd.unit_id`][flet_ads.BannerAd]
    - **Android**: `"ca-app-pub-3940256099942544/9214589741"`
    - **iOS**: `"ca-app-pub-3940256099942544/2435281174"`
* [`InterstitialAd.unit_id`][flet_ads.InterstitialAd]
    - **Android**: `"ca-app-pub-3940256099942544/1033173712"`
    - **iOS**: `"ca-app-pub-3940256099942544/4411468910"`

**They are not meant to be used in production.**

## Example

<CodeExample path={frontMatter.examples + '/example_1.py'} language="python" />

<Image src={frontMatter.example_images + '/example_1.gif'} width="55%" />
