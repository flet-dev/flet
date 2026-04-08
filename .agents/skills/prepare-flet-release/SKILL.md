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

Use [`write-changelog-entry`](../write-changelog-entry/SKILL.md) for drafting or refining individual changelog items.
That skill is the source of truth for item wording, scope selection, and what should or should not be mentioned in a single entry.

## Steps

* Take latest Flet release version from the repo and
  increment third (patch) digit to get the next version if it's a minor release
  or second (minor) digit if it's a major release.
* Pull the latest `main` and create a new branch named `prepare-release-{new_version}` from `main`.
* Set new version in packages/flet/pubspec.yaml.
* Run pub get in /client dir to refresh pubspec.lock with new version.
* Add new entries into `packages/flet/CHANGELOG.md` and `/CHANGELOG.md` from the git log since the last release.
  * Use [`write-changelog-entry`](../write-changelog-entry/SKILL.md) for every individual item.
  * Build the candidate set from relevant commits, PRs, and issues since the last release.
  * Ensure that all inferred PRs and issues in the changelog have the `{version}` milestone attached on GitHub.
  * If a related issue or PR is missing the `{version}` milestone, update the milestone on GitHub and keep the link in the changelog.
  * When selecting candidates for `packages/flet/CHANGELOG.md`, prefer items with meaningful Flutter-side impact.
  * When selecting candidates for `sdk/python/packages/*/CHANGELOG.md`, prefer published Python-facing changes; do not include extension-internal Flutter implementation work unless it materially changes user-visible Python behavior.
* Scan all changelogs for `Unreleased` sections, not only the root ones:
  * `/CHANGELOG.md`
  * `packages/flet/CHANGELOG.md`
  * `sdk/python/packages/*/CHANGELOG.md`
  Recommended check command:
  `rg -n "^##\\s*\\[?Unreleased\\]?|^##\\s*Unreleased" -S CHANGELOG.md packages/flet/CHANGELOG.md sdk/python/packages/*/CHANGELOG.md`
* If any changelog has an `Unreleased` section, convert that section into the new release section (`## {new_version}`), preserving and re-sorting its items. Do not leave duplicate release content in both `Unreleased` and `{new_version}`.
  This conversion must be done for every matched changelog from the scan above.
* Sort items in changelogs as following:
  * New features
  * Improvements
  * Bug fixes
  * Other changes (chore, refactor, etc.)
* Templates are in `sdk/python/templates/` and automatically packaged as zip artifacts with the GitHub Release. No manual branch creation in external repos is needed.
