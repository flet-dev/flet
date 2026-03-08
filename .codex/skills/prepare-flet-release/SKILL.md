---
name: prepare-flet-release
description: Use when asked to prepare new Flet release by bumping versions and author release notes.
---

## Inputs

* Previous Flet version from repo tags.
* Whether it's minor or major release.

## Related Skills

Use [`flet-deprecation`](../flet-deprecation/SKILL.md) when release prep includes:
- adding new deprecations in this release,
- removing APIs whose `delete_version` equals this release version,
- auditing changelog entries that mention deprecations/removals.

## Steps

* Take latest Flet release version from the repo and
  increment third (patch) digit to get the next version if it's a minor release
  or second (minor) digit if it's a major release.
* Set new version in packages/flet/pubspec.yaml.
* Run pub get in /client dir to refresh pubspec.lock with new version.
* Add a new entry into packages/flet/CHANGELOG.md from a git log since the last release. Do not add chore/trivial/duplicate items, add items with related issue or PR.
  As it's a Flutter package prefer items having changes on Flutter side.
* Add a new entry into /CHANGELOG.md. Do not add chore/trivial/duplicate items, add items with related issue or PR.
* If deprecations are part of the release:
  - ensure new deprecations follow the removal policy,
  - ensure removals are performed for items scheduled for this release,
  - reflect both in changelog notes with explicit versions.
* Check that `{new_version}` branch (without `v`, just version number) exists in `flet/flet-build-template` repository.
  If not, add/derive that branch from a previous version.
* Check that `{new_version}` branch (without `v`, just version number) exists in `flet/flet-app-templates` repository.
  If not, add/derive that branch from a previous version.
