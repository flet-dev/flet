---
examples: ../../examples/controls/ads
example_images: ../examples/controls/ads/media
---

# Ads

Displaying Google Ads in [Flet](https://flet.dev) apps.

Based on the [google_mobile_ads](https://pub.dev/packages/google_mobile_ads) Flutter package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

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

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

![example_1]({{ example_images }}/example_1.gif){width="80%"}
/// caption
///

## Packaging

The following are to be done when packaging an app that uses the `flet-ads` package.

### Specify AdMob app ID

Specify your [AdMob app ID](https://support.google.com/admob/answer/7356431), without which your application might crash
on launch.

You can specify the app ID in two ways:

- In your `pyproject.toml` file:

```toml
# for Android
[tool.flet.android.meta_data]
"com.google.android.gms.ads.APPLICATION_ID" = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"

# for iOS
[tool.flet.ios.info]
GADApplicationIdentifier = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```

- In your build command from the terminal:

```bash
# for Android
flet build apk ... --android-meta-data com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy

# for iOS
flet build ipa ... --info-plist GADApplicationIdentifier=ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy
```

/// admonition | Test Values
    type: tip
AdMob [provides](https://developers.google.com/admob/flutter/banner#always_test_with_test_ads) app and ad unit IDs for
testing purposes:

* AdMob app ID: `"ca-app-pub-3940256099942544~3347511713"`
* `BannerAd.unit_id` on **Android**: `"ca-app-pub-3940256099942544/9214589741"`
* `BannerAd.unit_id` on **iOS**: `"ca-app-pub-3940256099942544/2435281174"`
* `InterstitialAd.unit_id` on **Android**: `"ca-app-pub-3940256099942544/1033173712"`
* `InterstitialAd.unit_id` on **iOS**: `"ca-app-pub-3940256099942544/4411468910"`

Remember to replace these values with your own when you're ready to package your app.
///
