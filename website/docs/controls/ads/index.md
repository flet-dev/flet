---
examples: "extensions/ads"
example_images: "examples/extensions/ads/media"
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

- [setting Android permissions](../../publish/android.md#permissions)
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

- [setting iOS permissions](../../publish/ios.md#permissions)
- [AdMob app ID for testing purposes](#test-values)

### Test Values

AdMob [provides](https://developers.google.com/admob/flutter/banner#always_test_with_test_ads) app and ad unit IDs for
testing purposes.

* **AdMob app ID**: `"ca-app-pub-3940256099942544~3347511713"`
* [`BannerAd.unit_id`](bannerad.md)
    - **Android**: `"ca-app-pub-3940256099942544/9214589741"`
    - **iOS**: `"ca-app-pub-3940256099942544/2435281174"`
* [`InterstitialAd.unit_id`](interstitialad.md)
    - **Android**: `"ca-app-pub-3940256099942544/1033173712"`
    - **iOS**: `"ca-app-pub-3940256099942544/4411468910"`

**They are not meant to be used in production.**

## Consent (UMP)

[`ConsentManager`][flet_ads.ConsentManager] wraps Google's
[User Messaging Platform (UMP)](https://developers.google.com/admob/flutter/privacy) to
gather user consent (for example, the GDPR/EEA consent form) before requesting ads.

The consent message itself is created and published in the
[AdMob console](https://apps.admob.com), not in code: Google serves the
region-appropriate message (EEA/GDPR, a regulated US state, and so on) based on the user's
location. Your app only requests an update and shows the form when required.

### Testing the consent form

Force a geography during development with
[`DebugGeography`][flet_ads.DebugGeography] on
[`ConsentDebugSettings`][flet_ads.ConsentDebugSettings]:

- **Simulators and emulators are automatically registered as test devices**, so the debug
  geography applies on them **without** any
  [`test_identifiers`][flet_ads.ConsentDebugSettings.test_identifiers].
- On a **physical device**, register it first: call
  [`request_consent_info_update()`][flet_ads.ConsentManager.request_consent_info_update]
  once, then read the device's hashed ID from the **native** device log. Add that ID to
  `test_identifiers` and re-run.

The message carrying the hashed ID differs per platform:

**Android** (`adb logcat`):

```text
Use new ConsentDebugSettings.Builder().addTestDeviceHashedId("33BE2250B43518CCDA7DE426D04EE231")
to set this as a debug device.
```

**iOS** (Xcode console / Console.app):

```text
<UMP SDK>To enable debug mode for this device,
set: UMPDebugSettings.testDeviceIdentifiers = @[2077ef9a63d2b398840261c8221a0c9b]
```

### Interpreting consent status

[`ConsentStatus`][flet_ads.ConsentStatus] reflects whether a decision was
*collected*, not what the user chose — it becomes `OBTAINED` whether they consent
**or** decline. To gate ad loading, use [`can_request_ads()`][flet_ads.ConsentManager.can_request_ads];
when consent is declined the SDK simply serves non-personalized ads.

Furthermore, the consent status is cached across sessions, so the form is shown only once. When in testing/debug mode,
you can call [`ConsentManager.reset()`][flet_ads.ConsentManager.reset] to replay the flow as a
first-time user. The [test AdMob app ID](#test-values) provided above already has a sample consent message, so it
shows the form during testing; in production your own app ID needs a message **published** in the
AdMob console.

### Under age of consent

Setting [`tag_for_under_age_of_consent`][flet_ads.ConsentRequestParameters.tag_for_under_age_of_consent]
to `True` suppresses the consent form — users under the age of consent cannot be asked to
consent. Leave it unset (or `False`) while testing the form.

## Example

<CodeExample path={frontMatter.examples + '/banner_ad_and_interstitial_ad/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_1.gif'} width="55%" />
