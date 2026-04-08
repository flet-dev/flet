---
name: write-changelog-entry
description: Use when asked to add, revise, or review a changelog or release-notes entry in this repo. Inspect the existing changelog section style and the relevant PR, issue, and commit context first, then write a focused entry in the correct release section without overstating docs, tests, or chores unless they are the primary user-facing change.
---

## Purpose

Write a single changelog entry that matches the surrounding section's style and reflects the actual shipped change.

Use [`prepare-flet-release`](../prepare-flet-release/SKILL.md) for full release preparation across versions and files.

## Inputs

* Target changelog file, usually `/CHANGELOG.md` or `packages/flet/CHANGELOG.md`.
* Release version or section if the user specifies one.
* Relevant PR number, issue number, commit(s), or branch context.

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
   * Put issue links before PR links when both exist.
   * Use plain-text author attribution at the end: `by @login.`

## Repo-specific guidance

* Do not mention tests in changelog items unless the change itself is test infrastructure.
* Do not mention docs/examples unless documentation is the primary deliverable.
* Avoid words like `refactor`, `cleanup`, or `coverage` unless the section is `Other changes` and that is truly the point.
* If a PR includes one main feature plus supporting docs/tests, write only the main feature.
* If a PR title is too narrow or too broad, use the PR description and diff to calibrate the final wording.
* If an item touches multiple controls, only group them when the change is one coherent feature.

## Good patterns

* `* Add \`scrollable\` to \`NavigationRail\` for overflowed destinations ([#1923](...), [#6356](...)) by @login.`
* `* Make \`NavigationDrawerDestination.label\` accept custom controls and add \`NavigationDrawerTheme.icon_theme\` ([#6379](...), [#6395](...)) by @login.`

## Checks

Before finishing, verify:

* The item sits under the right release and section.
* The wording matches neighboring entries in length and tone.
* The sentence describes the primary user-facing change.
* Issue and PR links are present when available.
* Attribution is plain text and placed last.
