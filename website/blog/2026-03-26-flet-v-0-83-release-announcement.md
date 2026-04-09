---
slug: flet-v-0-83-release-announcement
title: "Flet 0.83.0: Faster diffs, leaner packages, road to 1.0"
authors: feodor
tags: [releases]
---

Flet 0.83.0 is here with major performance gains, a reworked packaging pipeline, and better project transparency - all part of our push toward a rock-solid 1.0.

Highlights in this release:

* Up to 6.7× faster control diffing for both imperative and declarative apps.
* Smarter `.update()` logic that eliminates redundant updates.
* Declarative field validation with `Annotated` types.
* Desktop binaries and build templates moved from PyPI to GitHub Releases - smaller installs, pinned versions.
* Better release traceability with milestones and pre-releases on GitHub.

{/* truncate */}

## How to upgrade

If you use pip:

```bash
pip install 'flet[all]' --upgrade
```

If you use uv with `pyproject.toml` and want to upgrade everything:

```bash
uv sync --upgrade
```

If you want to upgrade only Flet packages:

```bash
uv sync --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web
```

## Faster control diffing

Every time your app calls `page.update()` or rebuilds a declarative component, Flet computes a diff - the set of property changes to send to Flutter. In 0.83.0 we overhauled this mechanism for both programming styles, and the results are dramatic.

### Imperative apps

**Before:** every `page.update()` walked through *all* properties of every control and compared them to the previous snapshot - even properties you never touched. If your control has 20 properties and you changed one, Flet still compared all 20.

**After:** a new `Prop` descriptor tracks which properties were actually written since the last diff. When you set `button.text = "Click me"`, only `text` is flagged as dirty. On the next `page.update()`, Flet sends only the dirty properties to Flutter and skips the rest. Think of it like only checking the light switches you actually flipped, instead of walking through every room in the house.

### Declarative apps

**Before:** when a component rebuilt, Flet compared every field of the new control tree against the old one - including nested value objects like `Alignment`, `BorderRadius`, and `BoxDecoration`. Since these objects were recreated on every build, they always looked "new" even when nothing changed.

**After:** ~150 data types now use a new `@value` decorator that makes them comparable by content rather than identity. Combined with a two-pass diff that first checks structural changes and then compares only fields that actually differ, the diff skips unchanged subtrees entirely.

### Benchmarks

Measured on Python 3.14.2, Apple Silicon:

* Frozen controls with 20 fields, 2 changed: **3.2–3.4× faster** (100–300 controls).
* Mixed keyed/unkeyed lists: **1.9–2.0× faster**.
* Non-frozen rebuilt lists: **2.9–4.5× faster**.
* [Sunflower demo](https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/declarative/sunflower.py) (500 seeds): **6.7× faster**.

More info:

* PR: [#6296](https://github.com/flet-dev/flet/pull/6296)

## Smarter `.update()` logic

In previous versions, Flet automatically called `page.update()` at the end of every event handler. If your handler already called `.update()` explicitly - say, to show a spinner before starting work - the framework would fire a second, redundant update at the end. This double-update could cause visual glitches or wasted work.

0.83.0 tracks whether `.update()` was called during handler execution. If it was, the automatic update at the end is skipped. This also means that apps migrated "as is" from Flet 0.28.3 (where there was no auto-update) will behave as expected without changes.

More info:

* PR: [#6298](https://github.com/flet-dev/flet/pull/6298)
* Issue: [#6236](https://github.com/flet-dev/flet/issues/6236)

## Declarative field validation

Control fields can now declare validation rules inline using Python's `Annotated` types and a new `V` rule set. Instead of writing manual checks in `__init__` or `before_update()`, you express constraints declaratively:

```python
from typing import Annotated
from flet.core.validation import V

entries: Annotated[list, V.or_(V.empty, V.min_length(3))]
```

This keeps validation close to the field definition and makes it easier to reason about invariants at a glance. Deprecation warnings also get auto-generated admonitions in the docs, so deprecated fields are clearly flagged without manual documentation effort.

More info:

* PR: [#6278](https://github.com/flet-dev/flet/pull/6278)

## Packaging: client binaries to GitHub Releases

Until now, Flet desktop binaries (the Flutter client for Windows, macOS, and Linux) were bundled inside PyPI wheels. This made the wheels large and consumed significant PyPI storage. We can't ask PyPI team for storage increase forever! 😊

Starting with 0.83.0, the desktop client is downloaded on first run from GitHub Releases and cached locally at `~/.flet/client/`. The `flet-desktop` package is now a single, tiny, platform-independent wheel.

What this means for you:

* **Faster installs.** `pip install flet` downloads a small wheel instead of a platform-specific binary.
* **One package.** The separate `flet-desktop-light` package is gone - choose the "light" or "full" flavor via `FLET_DESKTOP_FLAVOR` env var or `[tool.flet]` in `pyproject.toml`. On Linux the "light" flavor is used by default if not specified.
* **Air-gapped setups.** Set `FLET_CLIENT_URL` to point at a local mirror if your environment can't reach GitHub.

More info:

* PR: [#6309](https://github.com/flet-dev/flet/pull/6309)

## Packaging: templates to GitHub Releases

The `flet-build-template` and `flet-app-templates` repositories have been consolidated into the main Flet monorepo and are now distributed as zip archives attached to each GitHub Release.

When you run `flet build` or `flet create`, the CLI downloads the template zip that matches your installed Flet version. **Versions are pinned** - even for pre-releases - so you always get templates compatible with your Flet version. No more mismatches between the framework and the build template.

For stable releases, the `flet` Flutter package is published to pub.dev as usual. For pre-releases, the build template references the exact commit SHA via a Git dependency - so `flet build` always compiles against the precise Flutter code that matches your Python package.

More info:

* PR: [#6331](https://github.com/flet-dev/flet/pull/6331)

## Better release traceability

We've improved how you can track what's in each release:

* **Pre-releases on GitHub.** Every dev build now creates a [GitHub Release](https://github.com/flet-dev/flet/releases) (e.g., `v0.83.0.dev6045`). You can browse pre-releases to see exactly which fixes and features landed in each build - no more guessing whether your bug fix is in the latest dev version.
* **Milestones on issues and PRs.** Issues and pull requests are now assigned to [milestones](https://github.com/flet-dev/flet/milestones?state=closed). Want to know when your issue was fixed? Check the milestone - it tells you the release version.

## Road to 1.0

We're working hard to make Flet a scalable, sustainable framework, and 0.83.0 reflects that commitment.

**Everything is automated.** Our CI pipeline handles building, testing, packaging, and publishing end-to-end. Every push to `main` triggers a full build of all platform binaries, runs the test suite, executes `flet build` for all targets, and publishes dev releases to GitHub and pub.dev. There are no manual steps.

**Comprehensive integration testing.** We now run 200+ integration tests on macOS across 12 parallel test suites - covering core controls, Material and Cupertino widgets, services, themes, extensions, and example apps. A full run takes about 85 minutes and catches regressions before they reach you. Integration suites for other platforms are coming!

**New documentation is coming.** We're moving back to Docusaurus for the Flet docs, which will bring a better reading experience, improved search, and easier contribution workflow. Stay tuned.

## Other changes and bug fixes

* Customizable scrollbars ([#6282](https://github.com/flet-dev/flet/issues/6282)).
* Scrollable `ExpansionPanelList` ([#6294](https://github.com/flet-dev/flet/issues/6294)).
* `SharedPreferences` now supports `int`, `float`, `bool`, and `list[str]` types ([#6267](https://github.com/flet-dev/flet/issues/6267)).
* Align Python defaults with Dart defaults across all packages ([#6330](https://github.com/flet-dev/flet/issues/6330)).
* Fix `ReorderableListView` event deserialization for `on_reorder_start`/`on_reorder_end` ([#6315](https://github.com/flet-dev/flet/issues/6315)).
* Skip micropip load for apps with `pyproject.toml` ([#6300](https://github.com/flet-dev/flet/issues/6300)).

## Conclusion

Flet 0.83.0 is a release about foundations: faster internals, cleaner packaging, and better tooling. These are the kinds of improvements that compound - every future release builds on a faster, more reliable base.

Try it in your apps and share feedback in [GitHub Discussions](https://github.com/flet-dev/flet/discussions) or on [Discord](https://discord.gg/dzWXP8SHG8).

Happy Flet-ing!
