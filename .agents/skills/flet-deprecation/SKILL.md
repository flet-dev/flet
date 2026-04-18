---
name: flet-deprecation
description: Use when adding or changing deprecations for Python controls/APIs in sdk/python/packages/, including V.deprecated fields, deprecated decorators, version lifecycle, and docs admonitions/labels.
---

## When To Use

Use this skill when you:
- deprecate a control/dataclass field with `Annotated[..., V.deprecated(...)]`,
- deprecate a function/method/class with `flet.utils.deprecated` helpers,
- update deprecation wording, versions, or removal timelines,
- verify docs rendering for deprecations (admonition + `deprecated` label).

Do not use this skill for non-deprecation validation logic; use
[`flet-validation`](../flet-validation/SKILL.md).

## Source Of Truth

- Runtime decorators and warning helpers: `sdk/python/packages/flet/src/flet/utils/deprecated.py`
- Field-level deprecation rule: `sdk/python/packages/flet/src/flet/utils/validation.py` (`V.deprecated`)
- Docs extraction/labeling extension: `sdk/python/packages/flet/src/flet/utils/griffe_deprecations.py`

## Deprecation Decision Order

Use this order and stop at the first option that fits:
1. Property/field deprecation: `Annotated[..., V.deprecated(...)]`.
2. Function/method deprecation: `@deprecated(...)`.
3. Class/control deprecation: `@deprecated_class(...)`.

Do not add parallel custom warning logic in `before_update()` when `V.deprecated`
already covers the field.

## Runtime Contract For Property Renames

Follow the non-copying model:
- Python sends both properties when both are set.
- Dart prefers the new property and uses old property as fallback.
- Python does not copy/synchronize old/new values in `before_update()`.

Removal phase:
- At `delete_version` cleanup, remove old Python property/deprecation and remove
  Dart fallback in the same migration.

## Removal Version Policy

- Default policy: remove deprecated APIs after 3 minor releases.
- Example: deprecated in `0.82.0` -> remove in `0.85.0`.
- Use that policy to set `delete_version` unless there is an approved exception.

## Target Release Audit

When working on a release for `{new_version}`, treat deprecations with
`delete_version == {new_version}` as mandatory audit items.

- Scan Python packages for `@deprecated(...)`, `@deprecated_class(...)`,
  and `V.deprecated(...)` entries whose `delete_version` equals `{new_version}`.
- Recommended check command:
  `rg -n 'delete_version\\s*=\\s*"{new_version}"|delete_version\\s*=\\s*\\x27{new_version}\\x27' -S sdk/python/packages`
- Treat every match as release-relevant work, not informational output.
- If matches are found, summarize the findings first and ask the human for approval
  before editing files or making removals.
- For each match, decide whether the deprecated API must be removed now,
  whether a prior removal was missed, or whether the deprecation timeline is incorrect.
- If removal is due, make the code, docs, and changelog updates in the same change.
- After the cleanup edits are ready, summarize the resulting diff and ask the human
  for approval before creating a commit.
- Once commit approval is received, batch all confirmed `{new_version}` cleanup
  edits into one grouped commit instead of splitting them across multiple commits.
  Use commit message format: `release: remove deprecated APIs for {new_version}`
- Do not consider the release prep complete while unresolved `{new_version}` removals remain.

## Authoring Rules

1. Always set `version`.
2. Set `delete_version` using the 3-minor policy by default.
3. Keep `reason` plain text for runtime warnings.
4. Use `docs_reason` for docs-only markdown text.
5. When a replacement exists, name that replacement API explicitly in `reason` and `docs_reason`.

### Field Pattern

```python
from typing import Annotated, Optional
from flet.utils.validation import V

class ExampleControl:
    old_prop: Annotated[
        Optional[str],
        V.deprecated(
            "new_prop",
            version="0.17.0",
            delete_version="0.20.0",
            reason="Use new_prop instead.",
            docs_reason="Use :attr:`new_prop` or [`new_prop`](../controls/examplecontrol.md#flet.ExampleControl.new_prop) instead.",
        ),
    ] = None
```

### Function/Method Pattern

```python
from flet.utils.deprecated import deprecated

class ExampleControl:
    @deprecated(
        reason="Use new_func instead.",
        docs_reason="Use :meth:`new_func` or [`new_func()`](../controls/examplecontrol.md#flet.ExampleControl.new_func) instead.",
        version="0.17.0",
        delete_version="0.20.0",
    )
    def old_func(self):
        ...
```

### Class/Control Pattern

```python
from flet.utils.deprecated import deprecated_class

@deprecated_class(
    reason="Use NewControl instead.",
    docs_reason="Use :class:`~flet.NewControl` or [`NewControl`](../controls/newcontrol.md)  instead.",
    version="0.17.0",
    delete_version="0.20.0",
)
class OldControl:
    ...
```

### Deprecated Property Pattern

```python
from flet.utils.deprecated import deprecated

class ExampleControl:
    @property
    @deprecated(
        reason="Use new_value instead.",
        docs_reason="Use :attr:`new_value` or [`new_value`](../controls/examplecontrol.md#flet.ExampleControl.new_value) instead.",
        version="0.17.0",
        delete_version="0.20.0",
    )
    def value(self):
        ...
```

## `reason` vs `docs_reason`

- Runtime warnings always use `reason`.
- Docs admonitions prefer `docs_reason`; fallback is `reason`.
- Keep markdown/cross-refs out of `reason` to avoid noisy runtime output.

### Cross-reference Rule Inside `docs_reason`

In `docs_reason`, use reST roles for simple references when the auto-derived label is
sufficient, and use Markdown links when you need more control over the displayed text.

See [`docs-conventions`](../docs-conventions/SKILL.md) for details on supported cross-ref patterns and their syntax.

## Docs Behavior Expectations

For supported patterns, docs should auto-render:
- a `Deprecated` admonition section,
- a `deprecated` label/badge on the item.

Do not duplicate with manual deprecation admonitions in docstrings unless there
is a special case not covered by the extension.

## Testing Guidance

Do not add one-off tests for every API that gets deprecated when it uses an
existing, already-tested pattern (`V.deprecated`, `@deprecated`, or
`@deprecated_class`). For routine deprecation metadata updates, rely on the
shared helper and docs extraction tests.

Add or update tests only when the change affects deprecation infrastructure or
introduces meaningful new behavior, for example:
- changing runtime warning formatting or stacklevel behavior,
- changing docs extraction/labeling behavior,
- adding a new deprecation pattern,
- adding custom compatibility behavior outside the standard helper,
- fixing a regression where an existing test would not have failed.

Prefer these locations for infrastructure tests:
- `sdk/python/packages/flet/tests/test_deprecated.py`
- `sdk/python/packages/flet/tests/test_griffe_deprecations.py`
- `sdk/python/packages/flet/tests/test_validation.py` (for `V.deprecated`)

## Common Pitfalls

- Putting markdown/cross-refs into runtime `reason`.
- Forgetting `delete_version` when a removal target is already known.
- Adding old/new value-copy logic in Python for rename migrations.
- Duplicating deprecation warnings in multiple lifecycle hooks manually.
- Broken cross-refs targets in `docs_reason`.
