---
examples: ../../examples/controls/ads
example_images: ../examples/controls/ads/media
---

# Ads

Displaying Google Ads in [Flet](https://flet.dev) apps.

Based on the [google_mobile_ads](https://pub.dev/packages/google_mobile_ads) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ❌       | ❌     | ❌     | ✅   | ✅       | ❌   |

## Usage

To use ads controls add `flet-ads` package to your project dependencies:

/// tab | uv
```bash
uv add flet-ads
```

///
/// tab | pip
```bash
pip install flet-ads  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Requirements

The following are required for ads to work properly:

### Specify AdMob app ID

Specify your [AdMob app ID](https://support.google.com/admob/answer/7356431), without which your application might crash
on launch.

/// tab | `flet build`
```bash
# Android
flet build apk --android-meta-data com.google.android.gms.ads.APPLICATION_ID="ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"

# iOS
flet build ipa --info-plist GADApplicationIdentifier="ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```
///
/// tab | `pyproject.toml`
```toml
# Android
[tool.flet.android.meta_data]
"com.google.android.gms.ads.APPLICATION_ID" = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"

# iOS
[tool.flet.ios.info]
GADApplicationIdentifier = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```
///

For more information on the above configuration options, see:
[Android](../publish/android.md#meta-data) and [iOS](../publish/ios.md#infoplist) `flet build` docs.

### Test Values

AdMob [provides](https://developers.google.com/admob/flutter/banner#always_test_with_test_ads) app and ad unit IDs for
testing purposes:

* AdMob app ID: `"ca-app-pub-3940256099942544~3347511713"`
* [`BannerAd` ][flet_ads.BannerAd]
    - **Android**: `"ca-app-pub-3940256099942544/9214589741"`
    - **iOS**: `"ca-app-pub-3940256099942544/2435281174"`
* [`InterstitialAd`][flet_ads.InterstitialAd]
    - **Android**: `"ca-app-pub-3940256099942544/1033173712"`
    - **iOS**: `"ca-app-pub-3940256099942544/4411468910"`

/// admonition | Note
Remember to replace these values with your own when you're ready to package your app.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

{{ image(example_images + "/example_1.gif", width="80%") }}
