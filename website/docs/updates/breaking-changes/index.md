---
title: "Breaking changes and deprecations"
---

# Breaking changes and deprecations

Breaking changes and deprecations are release changes that can require code,
dependency, or configuration updates when you upgrade. Removed APIs are listed
here as breaking changes. Deprecated APIs still work for now, but they are
scheduled for removal.

:::note
These breaking change and deprecation guides are accurate as of the release that
introduced the change. Later releases might add new APIs or additional migration
paths.

This page lists the guides created for each release.
:::

## By release

The following guides are available. They're sorted by release, with the most recent release first.
Each guide explains the change, the reason for it, and how to migrate your code.

### Released in Flet 0.86.0

#### Breaking changes

- [App files ship unpacked in a read-only bundle; storage dirs reworked](/docs/updates/breaking-changes/v0-86-0/app-files-unpacked-read-only-bundle)
- [Android: site-packages ship zipped; some packages need `extract_packages`](/docs/updates/breaking-changes/v0-86-0/android-extract-packages)
- [Android: `x86` removed from target architectures](/docs/updates/breaking-changes/v0-86-0/android-x86-arch-removed)
- [Default bundled Python version is now 3.14](/docs/updates/breaking-changes/v0-86-0/default-bundled-python-3-14)
- [App and packages are compiled to `.pyc` by default](/docs/updates/breaking-changes/v0-86-0/compile-on-by-default)
- [`flet.version.pyodide_version` and `PYODIDE_VERSION` removed](/docs/updates/breaking-changes/v0-86-0/removed-pyodide-version-export)
- [Flet protocol framing upgraded for DataChannel support](/docs/updates/breaking-changes/v0-86-0/data-channel-protocol-upgrade)

#### Deprecations

- [`flet build --clear-cache` flag deprecated](/docs/updates/breaking-changes/v0-86-0/deprecated-clear-cache-flag)

### Released in Flet 0.85.0

#### Breaking changes

- [Deprecated spacing and border helper functions removed](/docs/updates/breaking-changes/v0-85-0/removed-spacing-border-helpers)

#### Deprecations

- [`DragTargetEvent` coordinate fields deprecated](/docs/updates/breaking-changes/v0-85-0/deprecated-drag-target-event-coordinates)
- [`Video` control APIs deprecated](/docs/updates/breaking-changes/v0-85-0/deprecated-video-apis)
