---
class_name: flet_geolocator.Geolocator
examples: ../../examples/services/geolocator
---

# Geolocator

Access device location services in your [Flet](https://flet.dev) app using the `flet-geolocator` extension.
The control wraps Flutter's [`geolocator`](https://pub.dev/packages/geolocator) package and exposes async helpers for permission checks and position streams.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add `flet-geolocator` to your project dependencies:

/// tab | uv
```bash
uv add flet-geolocator
```

///
/// tab | pip
```bash
pip install flet-geolocator  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Requirements

The below sections show the required configurations for each platform.

### Android

Configuration to be made to access the device's location:

- [`ACCESS_FINE_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#ACCESS_FINE_LOCATION): Allows access precise location. Will be preferred over `ACCESS_COARSE_LOCATION`, if both are set.
- [`ACCESS_COARSE_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#ACCESS_COARSE_LOCATION): Allows access approximate location.
- [`ACCESS_BACKGROUND_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#ACCESS_BACKGROUND_LOCATION) (optional): Allows access to location even when the app is in the background. Effective as from Android 10 (API level 29).
- [`FOREGROUND_SERVICE_LOCATION`](https://developer.android.com/reference/android/Manifest.permission#FOREGROUND_SERVICE_LOCATION) (optional): Allows access to location even when the app is in the foreground. Effective as from Android 14 (API level 34).

/// admonition | Note
    type: note
- At least one of `ACCESS_FINE_LOCATION` or `ACCESS_COARSE_LOCATION` permission is **required** to get location updates, with the former being preferred if both are set.
- Specifying the `ACCESS_COARSE_LOCATION` permission results in location updates with
    accuracy approximately equivalent to a city block. It might take a long time (minutes)
    before you will get your first locations fix as `ACCESS_COARSE_LOCATION` will only use
    the network services to calculate the position of the device. More information
    [here](https://developer.android.com/training/location/retrieve-current#permissions).
///

/// tab | `flet build`
```bash
flet build apk \
  --android-permissions android.permission.ACCESS_FINE_LOCATION=True \
      android.permission.ACCESS_COARSE_LOCATION=True \
      android.permission.ACCESS_BACKGROUND_LOCATION=True \
      android.permission.FOREGROUND_SERVICE_LOCATION=True
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.permission]
"android.permission.ACCESS_FINE_LOCATION" = true
"android.permission.ACCESS_COARSE_LOCATION" = true
"android.permission.ACCESS_BACKGROUND_LOCATION" = true
"android.permission.FOREGROUND_SERVICE_LOCATION" = true
```
///

See also:
- [setting Android permissions](../publish/android.md#permissions)

### iOS

Configuration to be made to access the device's location:

/// tab | `flet build`
```bash
flet build ipa \
  --info-plist NSLocationWhenInUseUsageDescription="Some message to describe why you need this permission..."
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.ios.info]
NSLocationWhenInUseUsageDescription = "Some message to describe why you need this permission..."
```
///

See also:
- [setting iOS permissions](../publish/ios.md#permissions)

### macOS

Configuration to be made to access the device's location:

/// tab | `flet build`
```bash
flet build macos \
  --info-plist NSLocationUsageDescription="Some message to describe why you need this permission..." \
  --macos-entitlements com.apple.security.personal-information.location=True
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.macos.info]
NSLocationUsageDescription = "Some message to describe why you need this permission..."

[tool.flet.macos.entitlement]
"com.apple.security.personal-information.location" = true
```
///

See also:
- [macOS permissions](../publish/macos.md#permissions)
- [macOS entitlements](../publish/macos.md#entitlements)

### Cross-platform

Additionally/Alternatively, you can make used of our predefined cross-platform `location`
[permission bundle](../publish/index.md#predefined-cross-platform-permission-bundles):

/// tab | `flet build`
```bash
flet build <target_platform> --permissions location
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
permissions = ["location"]
```
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
