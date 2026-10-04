---
title: "macOS and iOS: built apps now require macOS 12 and iOS 15"
---

# macOS and iOS: built apps now require macOS 12 and iOS 15

:::note
This guide is accurate as of Flet 1.0.4. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Starting with Flet 1.0.4, apps built with `flet build macos` require **macOS 12
(Monterey) or later**, and apps built with `flet build ipa` or
`flet build ios-simulator` require **iOS 15 or later**. Previously the
[build template](../../../publish/index.md#build-template) targeted macOS 11 and
iOS 13.

The Flet desktop client, which `flet run` and `ft.run()` use to show desktop
apps on macOS, now requires macOS 12 as well, as the
[installation requirements](../../../getting-started/installation.md#macos)
already stated.

## Background

Xcode 27 only builds for macOS 12.0 or later and iOS 15.0 or later. A lower
deployment target, which Xcode 26 and earlier only warned about, is now a build
error, so `flet build`, `flet debug` and `flet test` failed for macOS and iOS on
Xcode 27 ([#6874](https://github.com/flet-dev/flet/issues/6874)):

```
The macOS deployment target 'MACOSX_DEPLOYMENT_TARGET' is set to 11.0, but the range of supported deployment target versions is 12.0 to 27.0.x.
```

Flet 1.0.4 raises the deployment targets in the build template and the desktop
client to these minimums. They are also the minimums of Flutter 3.47 and later.

## Who is affected

- **iOS**: every iPhone and iPad that runs iOS 13 or 14 can be updated to iOS 15,
  so no device loses support. Only devices that were never updated past iOS 14
  can't install the new build.
- **macOS**: Macs that can't be updated past macOS 11 can no longer
  run your app. These are some models from 2013-2015, such as the MacBook Air
  (Mid 2013, Early 2014), the MacBook Pro (Late 2013, Mid 2014) and the iMac
  (Mid 2014). See [macOS Monterey compatible computers](https://support.apple.com/HT212551)
  for the full list. On macOS 11, the app doesn't open, and macOS says that it
  requires a newer macOS version.

## Migration guide

Most projects need no changes: rebuild your app with Flet 1.0.4 or later. After
the upgrade, the next build regenerates the project in your `build` directory
from the new template.

### Custom build templates

If you build with your own template (`--template` or
[`[tool.flet.template]`](../../../publish/index.md#build-template)), apply the
same changes to it, or it will still fail on Xcode 27.

In `macos/Podfile`, raise the platform and let pods that target an older macOS
inherit it:

```ruby
platform :osx, '12.0'

# ...

post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_macos_build_settings(target)
    if target.deployment_target.to_s[/\d+/].to_i < 12
      target.build_configurations.each do |config|
        config.build_settings.delete('MACOSX_DEPLOYMENT_TARGET')
      end
    end
  end
end
```

In `macos/Runner.xcodeproj/project.pbxproj`, set all three occurrences (Debug,
Release and Profile) to:

```
MACOSX_DEPLOYMENT_TARGET = 12.0;
```

Do the same for iOS in `ios/Podfile`:

```ruby
platform :ios, '15.0'

# ...

post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
    if target.deployment_target.to_s[/\d+/].to_i < 15
      target.build_configurations.each do |config|
        config.build_settings.delete('IPHONEOS_DEPLOYMENT_TARGET')
      end
    end
  end
end
```

and in `ios/Runner.xcodeproj/project.pbxproj`:

```
IPHONEOS_DEPLOYMENT_TARGET = 15.0;
```

Keep any other code you already have in `post_install`. The pod step is needed
because Flutter 3.44 creates its own engine pods for macOS 10.15 and iOS 13.0.
Flutter 3.47 and later handle this themselves.

### Supporting macOS 11 or iOS 13-14

Builds for these versions need Xcode 26 or earlier, together with Flet 1.0.3 or
a custom template that keeps the old deployment targets. For iOS this is a
short-term option: starting April 2027, App Store Connect only accepts iOS apps
built with the iOS 27 SDK, which comes with Xcode 27
([announcement](https://developer.apple.com/news/?id=k1mtkt1k)).

### No action needed for

- Android, Windows, Linux and web apps.

## Timeline

- Changed in: `1.0.4`

## References

- Docs: [Minimum macOS version](../../../publish/macos.md#minimum-macos-version),
  [Minimum iOS version](../../../publish/ios.md#minimum-ios-version)
- Issue: [#6874](https://github.com/flet-dev/flet/issues/6874)
- Pull request: [#6914](https://github.com/flet-dev/flet/pull/6914)
- [Flutter supported platforms](https://docs.flutter.dev/reference/supported-platforms)
- Release notes: [Flet 1.0.4](../../release-notes.md)
