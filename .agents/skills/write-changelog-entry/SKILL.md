---
name: write-changelog-entry
description: Use when asked to add, revise, or review a changelog or release-notes entry in this repo. Inspect the existing changelog section style and the relevant PR, issue, and commit context first, then write a focused entry in the correct release section without overstating docs, tests, or chores unless they are the primary user-facing change.
---

## Purpose

Write a single changelog entry that matches the surrounding section's style and reflects the actual shipped change.

## Inputs

* Target changelog file, usually `/CHANGELOG.md` or `packages/flet/CHANGELOG.md`.
* Release version or section if the user specifies one.
* Relevant PR number, issue number, commit(s), or branch context.

## Target file selection

Choose the narrowest correct changelog file before writing the item.

* Use `/CHANGELOG.md` for repo-level or broadly user-facing Flet changes.
* Use `packages/flet/CHANGELOG.md` only for changes relevant to Flutter package
  consumers and extension developers. Do not mirror `/CHANGELOG.md` entries there
  just because a user-facing feature required Flutter-side implementation.
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

## Workflow

1. Inspect the target changelog section before editing.
   * Match the existing headings and item style exactly.
   * In this repo, preferred buckets are:
     * `### New features`
     * `### Improvements`
     * `### Bug fixes`
     * `### Other changes`
2. Inspect the source of truth for scope.
   * Prefer PR title and PR description/summary over commit noise.
   * Use linked issues to understand user-facing intent.
   * Use commits only to confirm details or fill gaps.
3. Extract the primary shipped change.
   * Lead with the API, control, command, or behavior that changed.
   * Mention docs, examples, tests, refactors, or chores only when they are the main outcome the user would care about.
4. Write one concise item.
   * Avoid laundry lists unless the PR truly shipped multiple peer-level features.
   * Prefer concrete nouns and verbs over implementation detail.
   * Keep the sentence focused on what users gained or what was fixed.
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
* Add `packages/flet/CHANGELOG.md` entries for public Dart APIs, extension authoring
  contracts, shared Dart utility behavior, serialization/parsing contracts that custom
  controls rely on, or Flutter dependency/compatibility changes.

## Good patterns

* `* Add \`scrollable\` to \`NavigationRail\` for overflowed destinations ([#1923](...), [#6356](...)) by @login.`
* `* Make \`NavigationDrawerDestination.label\` accept custom controls and add \`NavigationDrawerTheme.icon_theme\` ([#6379](...), [#6395](...)) by @login.`

## Checks

Before finishing, verify:

* The item sits under the right release and section.
* The wording matches neighboring entries in length and tone.
* The sentence describes the primary user-facing change.
* Issue and PR links follow repo style, including issue-only direct-commit cases.
* Attribution is plain text and placed last.
