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
* Pull the latest `main` and create a new branch named `prepare-release-{new_version}` from `main`.
* Set new version in packages/flet/pubspec.yaml.
* Run pub get in /client dir to refresh pubspec.lock with new version.
* Add a new entry into packages/flet/CHANGELOG.md from a git log since the last release. Go through all commits and collect all mentioned issues and pull requests. There could be several issues done in a single PR (commit) - group them by creating a single descriptive change/fix/feature item and put all issues and PR links in `[#<issue_number>](<issue_url>)` format in braces next to it. Do not add chore/trivial/duplicate items.
  Every changelog item must include both related issue link(s) and PR link(s) when available (issue first, PR second). If no issue exists, include PR link(s) only.
  Also include issue-only items when a change was done via direct commit without PR (for example, an issue referenced in commit context but no PR exists).
  Every changelog item must include author attribution as a GitHub profile link: `by [@<github_login>](https://github.com/<github_login>)`.
  Place attribution at the end of each item after links, for example:
  `* Added feature X ([#123](...), [#456](...)) by [@contributor](https://github.com/contributor).`
  Use PR author login for PR-based items. For issue-only direct-commit items, use the commit author GitHub login if available.
  If one item groups multiple PRs by different authors, attribute all relevant authors:
  `by [@user1](https://github.com/user1), [@user2](https://github.com/user2)`.
  Ensure that all inferred PRs and issues in the changelog have `{version}` milestone attached on GitHub.
  If a related issue or PR is missing the `{version}` milestone, update the milestone on GitHub and keep the link in the changelog; do not omit issue links just because milestone metadata is missing.
  As it's a Flutter package prefer items having changes on Flutter side.
* Add a new entry into /CHANGELOG.md. Do not add chore/trivial/duplicate items, add "worth while" items with related issue or PR.
  Every changelog item must include both related issue link(s) and PR link(s) when available (issue first, PR second). If no issue exists, include PR link(s) only.
  Also include issue-only items when a change was done via direct commit without PR (for example, an issue referenced in commit context but no PR exists).
  Every changelog item must include author attribution as a GitHub profile link: `by [@<github_login>](https://github.com/<github_login>)`.
  Use PR author login for PR-based items. For issue-only direct-commit items, use the commit author GitHub login if available.
  If a related issue or PR is missing the `{version}` milestone, update the milestone on GitHub and keep the link in the changelog; do not omit issue links just because milestone metadata is missing.
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
