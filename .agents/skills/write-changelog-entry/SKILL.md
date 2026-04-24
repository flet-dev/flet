---
name: write-changelog-entry
description: Use when asked to add, revise, or review a changelog or release-notes entry in this repo. Inspect the existing changelog section style and the relevant PR, issue, and commit context first, then write a focused entry in the correct release section without overstating docs, tests, or chores unless they are the primary user-facing change.
---

## Purpose

Write changelog entries that match the surrounding section's style and reflect the actual shipped change for the intended audience.

## Inputs

* Target changelog file, if specified; otherwise infer it from the changed package
  and audience.
* Release version or section if the user specifies one.
* Relevant PR number, issue number, commit(s), or branch context.

## Target file selection

Choose the narrowest correct changelog file before writing entries.

* Use `/CHANGELOG.md` for repo-level or broadly user-facing Flet changes.
* Use `packages/flet/CHANGELOG.md` only for changes relevant to Flutter package
  consumers and extension developers. See the dedicated section below.
* Use `sdk/python/packages/<package>/CHANGELOG.md` for changes scoped to a specific
  Python package.
* For extension (ex: flet-audio) changelogs under
  `sdk/python/packages/<package>/CHANGELOG.md`, write
  entries from the published Python user's perspective. Do not surface internal Flutter
  implementation changes unless they materially change the Python-facing feature,
  behavior, or API.
* If one change clearly belongs in more than one published surface, update each relevant
  changelog file.
* Do not default everything to `/CHANGELOG.md` when a package-specific changelog is the
  better fit.

## Root vs Flutter package changelog

`/CHANGELOG.md` and `packages/flet/CHANGELOG.md` have different audiences.

* `/CHANGELOG.md` is the broad Flet product changelog. Write entries from the app
  developer's perspective, usually summarizing the shipped feature or fix at about
  PR-title specificity.
* `packages/flet/CHANGELOG.md` is for Flutter package consumers and extension
  developers. Write entries only when they need to know a specific Dart-side API,
  utility, parser, serializer, runtime contract, dependency, or compatibility change.
* Do not repeat a root changelog entry in `packages/flet/CHANGELOG.md` merely because
  the implementation touched Dart files.
* If both audiences are affected, update both changelogs, but phrase them differently:
  the root entry should describe the user-facing outcome, while the Flutter package
  entry should describe the precise Dart/extension-facing change.

Example split:

* Root: `Add support for text-or-control labels in \`NavigationDestination\`s.`
* Flutter package, only if applicable: `Extend \`Control\` with \`.buildTextOrWidget()\` to parse properties that accept either plain text or child controls.`

## Workflow

1. Inspect the target changelog section before editing.
   * Match the existing headings and item style exactly.
   * In this repo, preferred buckets are:
     * `### New features`
     * `### Improvements`
     * `### Bug fixes`
     * `### Other changes`
2. Inspect the source of truth for scope and audience.
   * Prefer PR title and PR description/summary over commit noise.
   * Use linked issues to understand user-facing intent.
   * Use commits only to confirm details or fill gaps.
3. Extract the primary shipped change.
   * Lead with the API, control, command, or behavior that changed.
   * Mention docs, examples, tests, refactors, or chores only when they are the main outcome the changelog audience would care about.
4. Write concise item(s) for the selected changelog(s).
   * Avoid laundry lists unless the PR truly shipped multiple peer-level features.
   * Prefer concrete nouns and verbs over implementation detail.
   * Keep each sentence focused on what that changelog's audience gained or must know.
5. Add links and attribution in repo style.
   * Include both related issue link(s) and PR link(s) when available, with issue links
     first.
   * If no issue exists, include PR link(s) only.
   * Include issue-only direct-commit items when a shipped change has no PR.
   * Use plain-text author attribution at the end: `by @login.`
   * Use the PR author login for PR-based items.
   * For issue-only direct-commit items, use the commit author login if available.
   * If one item groups multiple PRs by different authors, attribute all relevant
     authors: `by @user1, @user2.`

## Repo-specific guidance

* Do not mention tests in changelog items unless the change itself is test infrastructure.
* Do not mention docs/examples unless documentation is the primary deliverable.
* Avoid words like `refactor`, `cleanup`, or `coverage` unless the section is `Other changes` and that is truly the point.
* If a PR includes one main feature plus supporting docs/tests, write only the main feature.
* If a PR title is too narrow or too broad, use the PR description and diff to calibrate the final wording.
* If an item touches multiple controls, only group them when the change is one coherent feature.
* Do not add chore, trivial, or duplicate items to user-facing release notes.
* For extension package changelogs, prefer Python-facing API, behavior, packaging, and
  usability changes over Flutter implementation details that are not directly published
  to users.

## Good patterns

Root changelog:

* `* Add \`scrollable\` to \`NavigationRail\` for overflowed destinations ([#1923](...), [#6356](...)) by @login.`
* `* Make \`NavigationDrawerDestination.label\` accept custom controls and add \`NavigationDrawerTheme.icon_theme\` ([#6379](...), [#6395](...)) by @login.`

Flutter package changelog:

* `* Improve \`parseBool()\` to accept string and numeric payload values ([#1234](...)) by @login.`
* `* Extend \`Control\` with \`.buildTextOrWidget()\` to parse properties that accept either strings or child controls ([#1234](...)) by @login.`
* `* Improve extension asset resolution to avoid package path collisions ([#1234](...)) by @login.`
* `* Add \`parseEnum()\` utility for consistent enum parsing ([#1234](...)) by @login.`

## Checks

Before finishing, verify:

* The item sits under the right release and section.
* The wording matches neighboring entries in length and tone.
* The sentence describes the primary change for that changelog's audience.
* `packages/flet/CHANGELOG.md` entries are specific to Dart/Flutter package or
  extension-facing behavior and are not bare repeats of root changelog entries.
* Issue and PR links follow repo style, including issue-only direct-commit cases.
* Attribution is plain text and placed last.
