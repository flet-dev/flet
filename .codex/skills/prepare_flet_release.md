# Skill: Prepare new Flet release

## Purpose

Bump versions and author release notes.

## Inputs

* Previous Flet version from repo tags.
* Whether it's minor or major release.

## Steps

* Take latest Flet release version from the repo and
  increment third (patch) digit to get the next version if it's a minor release
  or second (minor) digit if it's a major release.
* Set new version in packages/flet/pubspec.yaml.
* Run pub get in /client dir to refresh pubspec.lock with new version.
* Add a new entry into packages/flet/CHANGELOG.md from a git log since the last release. Do not add chore/trivial/duplicate items, add items with related issue or PR.
  As it's a Flutter package prefer items having changes on Flutter side.
* Add a new entry into /CHANGELOG.md. Do not add chore/trivial/duplicate items, add items with related issue or PR.
* Check that `{new_version}` branch (without `v`, just version number) exists in `flet/flet-build-template` repository.
  If not, add/derive that branch from a previous version.
* Check that `{new_version}` branch (without `v`, just version number) exists in `flet/flet-app-templates` repository.
  If not, add/derive that branch from a previous version.
