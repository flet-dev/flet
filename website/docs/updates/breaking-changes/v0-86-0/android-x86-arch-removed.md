---
title: "Android: x86 removed from target architectures"
---

# Android: `x86` removed from target architectures

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

The 32-bit `x86` ABI is no longer a valid Android target architecture. Starting with Flet 0.86.0,
`flet build apk` / `aab` validates the requested architectures upfront, and a build that includes
`x86` — via `--arch`, `[tool.flet.android].target_arch`, or `[tool.flet].target_arch` — fails
immediately with:

```
Invalid Android architecture(s): x86.
Supported: armeabi-v7a, arm64-v8a, x86_64.
```

In earlier Flet versions `x86` was listed as a supported value and accepted without error — but it
never produced a working app for x86 devices: Flutter has no x86 release (AOT) support and has
since removed the target entirely, and the bundled CPython distributions were never built for
x86. The value was silently passed through and effectively ignored.

## Background

Flet 0.86.0 reworked the Android build pipeline (see the
[`extract_packages` guide](android-extract-packages.md)): requested ABIs are now explicitly mapped
to Flutter `--target-platform` values and to bundled Python distributions, so an ABI that neither
Flutter nor Python supports is rejected at the start of the build instead of silently doing
nothing. `x86` has also been removed from the build templates and documentation throughout.

## Migration guide

Remove `x86` from your architecture lists:

```toml
[tool.flet.android]
target_arch = ["arm64-v8a", "armeabi-v7a", "x86_64"]  # drop "x86"
```

or from the command line:

```bash
flet build apk --arch arm64-v8a x86_64
```

Nothing is lost by dropping it — previous builds never shipped a working x86 app. If you were
targeting x86 for Android *emulators*, use an `x86_64` (or `arm64-v8a`) emulator system image
instead; x86 images are only published for long-obsolete API levels.

All three supported ABIs — `arm64-v8a`, `x86_64`, and `armeabi-v7a` — are available for
every [bundled Python version](../../../publish/index.md#choosing-a-python-version); see
[supported target architectures](../../../publish/android.md#supported-target-architectures).

## Timeline

- Changed in: `0.86.0`

## References

- [Android: supported target architectures](../../../publish/android.md#supported-target-architectures)
- [Flutter Android deployment docs](https://docs.flutter.dev/deployment/android)
- Release notes: [Flet 0.86.0](../../release-notes.md)
