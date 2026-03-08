---
name: prepare-flet-release
description: Use when asked to prepare new Flet release by bumping versions and author release notes.
---

## Inputs

* Previous Flet version from repo tags.
* Whether it's minor or major release.

## Steps

* Take latest Flet release version from the repo and
  increment third (patch) digit to get the next version if it's a minor release
  or second (minor) digit if it's a major release.
* Set new version in packages/flet/pubspec.yaml.
* Run pub get in /client dir to refresh pubspec.lock with new version.
* Add a new entry into packages/flet/CHANGELOG.md from a git log since the last release. Go through all commits and collect all mentioned issues and pull requests. There could be several issues done in a single PR (commit) - group them by creating a single descriptive change/fix/feature item and put all issues and PR links in `[#<issue_number>](<issue_url>)` format in braces next to it. Do not add chore/trivial/duplicate items.
  Every changelog item must include both related issue link(s) and PR link(s) when available (issue first, PR second). If no issue exists, include PR link(s) only.
  Also include issue-only items when a change was done via direct commit without PR (for example, an issue referenced in commit context but no PR exists).
  As it's a Flutter package prefer items having changes on Flutter side.
* Add a new entry into /CHANGELOG.md. Do not add chore/trivial/duplicate items, add "worth while" items with related issue or PR.
  Every changelog item must include both related issue link(s) and PR link(s) when available (issue first, PR second). If no issue exists, include PR link(s) only.
  Also include issue-only items when a change was done via direct commit without PR (for example, an issue referenced in commit context but no PR exists).
* If any changelog has an `Unreleased` section, convert that section into the new release section (`## {new_version}`), preserving and re-sorting its items. Do not leave duplicate release content in both `Unreleased` and `{new_version}`.
* Sort items in changelogs as following:
  * New features
  * Improvements
  * Bug fixes
  * Other changes (chore, refactor, etc.)
* Check that `{new_version}` branch (without `v`, just version number) exists in `flet/flet-build-template` repository.
  If not, add/derive that branch from a previous version.
* Check that `{new_version}` branch (without `v`, just version number) exists in `flet/flet-app-templates` repository.
  If not, add/derive that branch from a previous version.
