---
title: "Compatibility policy"
---

# Compatibility policy

Flet tries to balance API stability with the need to keep improving the
framework, fixing bugs, and simplifying APIs before and after Flet 1.0.

## Breaking changes

A breaking change is a change that can require users to update app code,
configuration, dependencies, or build settings when upgrading Flet.

Examples include:

- removing a public API;
- changing a default behavior in a way that affects existing apps;
- changing event payloads or method return values;
- changing minimum supported Python, Flutter, platform, or dependency versions;
- changing build, packaging, or publishing requirements.

When a breaking change needs migration guidance, it should be listed in
[Breaking changes and deprecations](breaking-changes/index.md) and linked from
[Release notes](release-notes.md).

## Deprecation policy

When possible, Flet deprecates APIs before removing them. Deprecated APIs remain
available during the deprecation period, emit runtime warnings where supported,
and appear with deprecation labels in API docs.

By default, deprecated APIs are removed after three minor releases. For example,
an API deprecated in `0.85.0` is normally scheduled for removal in `0.88.0`.

Exceptions can happen when a deprecation needs more migration time or when
compatibility would block an important fix. Any exception should be called out
in the related release notes or migration guide.

## Where changes are documented

- [Release notes](release-notes.md) list each release and link to announcements,
  changelogs, and migration guides.
- [Breaking changes and deprecations](breaking-changes/index.md) explain changes
  that require migration.
- [Breaking changes and deprecations](breaking-changes/index.md) lists
  release-specific breaking changes and deprecation guides.
- API reference pages show deprecation details next to affected APIs.
