---
class_name: "flet_geolocator.Geolocator"
examples: "extensions/geolocator"
title: "Geolocator"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Geolocator

Access device location services in your [Flet](https://flet.dev) app using the `flet-geolocator` extension.
The control wraps Flutter's [`geolocator`](https://pub.dev/packages/geolocator) package and exposes async helpers for permission checks and position streams.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add `flet-geolocator` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-geolocator
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-geolocator  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Requirements

The below sections show the required configurations for each platform.

### Android

Configuration to be made to access the device's location:

- [`ACCESS_FINE_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#ACCESS_FINE_LOCATION): Allows access precise location. Will be preferred over `ACCESS_COARSE_LOCATION`, if both are set.
- [`ACCESS_COARSE_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#ACCESS_COARSE_LOCATION): Allows access approximate location.
- [`ACCESS_BACKGROUND_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#ACCESS_BACKGROUND_LOCATION) (optional): Allows access to location even when the app is in the background. Effective as from Android 10 (API level 29).
- [`FOREGROUND_SERVICE_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#FOREGROUND_SERVICE_LOCATION) (optional): Allows access to location even when the app is in the foreground. Effective as from Android 14 (API level 34).

:::note[Note]
- At least one of `ACCESS_FINE_LOCATION` or `ACCESS_COARSE_LOCATION` permission is **required** to get location updates, with the former being preferred if both are set.
- Specifying the `ACCESS_COARSE_LOCATION` permission results in location updates with
    accuracy approximately equivalent to a city block. It might take a long time (minutes)
    before you will get your first locations fix as `ACCESS_COARSE_LOCATION` will only use
    the network services to calculate the position of the device. More information
    [here](https://developer.android.com/training/location/retrieve-current#permissions).
:::

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-permissions android.permission.ACCESS_FINE_LOCATION=true \
  --android-permissions android.permission.ACCESS_COARSE_LOCATION=true \
  --android-permissions android.permission.ACCESS_BACKGROUND_LOCATION=true \
  --android-permissions android.permission.FOREGROUND_SERVICE_LOCATION=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.permission]
"android.permission.ACCESS_FINE_LOCATION" = true
"android.permission.ACCESS_COARSE_LOCATION" = true
"android.permission.ACCESS_BACKGROUND_LOCATION" = true
"android.permission.FOREGROUND_SERVICE_LOCATION" = true
```
</TabItem>
</Tabs>
See also:

- [setting Android permissions](../../publish/android.md#permissions)

### iOS

Configuration to be made to access the device's location:

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build ipa \
  --info-plist NSLocationWhenInUseUsageDescription="Some message to describe why you need this permission..."
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.ios.info]
NSLocationWhenInUseUsageDescription = "Some message to describe why you need this permission..."
```
</TabItem>
</Tabs>
See also:

- [setting iOS Info.plist entries](../../publish/ios.md#infoplist)

### macOS

Configuration to be made to access the device's location:

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos \
  --info-plist NSLocationUsageDescription="Some message to describe why you need this permission..." \
  --macos-entitlements com.apple.security.personal-information.location=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.info]
NSLocationUsageDescription = "Some message to describe why you need this permission..."

[tool.flet.macos.entitlement]
"com.apple.security.personal-information.location" = true
```
</TabItem>
</Tabs>
See also:

- [macOS permissions](../../publish/macos.md#permissions)
- [macOS entitlements](../../publish/macos.md#entitlements)

### Cross-platform

Additionally/alternatively, you can make use of our predefined cross-platform `location`
[permission bundle](../../publish/index.md#predefined-cross-platform-permission-bundles):

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build <target_platform> --permissions location
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet]
permissions = ["location"]
```
</TabItem>
</Tabs>
## Web: cached vs. fresh positions

On the web, `Geolocator.get_current_position` accepts a position from the
browser's cache up to **5 minutes old by default**, otherwise it asks the
browser for a fresh fix and times out after 30 seconds if none arrives. This
default exists because desktop browsers' on-demand location pipeline is slow
and frequently fails on stationary devices.

If you need stricter freshness (or a longer cache window), pass a
[`GeolocatorWebConfiguration`](./types/geolocatorwebconfiguration.md) with an
explicit `maximum_age` and/or `time_limit`:

```python
geo = ftg.Geolocator(
    configuration=ftg.GeolocatorWebConfiguration(
        accuracy=ftg.GeolocatorPositionAccuracy.HIGH,
        maximum_age=ft.Duration(seconds=10),
        time_limit=ft.Duration(seconds=15),
    ),
)
```

## Troubleshooting

### macOS: web browser returns `POSITION_UNAVAILABLE` or never resolves

When running a Flet app in `--web` mode on macOS, the browser may fail to obtain
a position even though Location Services is on and the browser is allowed in
*System Settings → Privacy & Security → Location Services*. Symptoms include:

- `getCurrentPosition` hanging or returning a `Location request timed out.` error.
- The position stream emitting `Failed to obtain position: Position update is unavailable`
  (this is the W3C `POSITION_UNAVAILABLE` / error code 2 from the browser).

This is a known issue with macOS' `locationd` daemon getting into a stuck state
where it reports the browser as authorized but never delivers a fix. Restart it:

```bash
sudo killall locationd
```

The daemon respawns automatically. You can verify the browser side independently
by visiting [browserleaks.com/geo](https://browserleaks.com/geo) — if that page
also fails to obtain a position, the problem is with the OS, not your Flet app.

The native (non-web) macOS Flet app is unaffected because it uses CoreLocation
directly through the platform plugin rather than going through the browser's
Geolocation API.

## Example

<CodeExample path={frontMatter.examples + '/example_1/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
