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

- Runtime decorators and warning helpers:
  `sdk/python/packages/flet/src/flet/utils/deprecated.py`
- Field-level deprecation rule:
  `sdk/python/packages/flet/src/flet/utils/validation.py` (`V.deprecated`)
- Docs extraction/labeling extension:
  `sdk/python/packages/flet/src/flet/utils/griffe_deprecations.py`

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

## Authoring Rules

1. Always set `version`.
2. Set `delete_version` using the 3-minor policy by default.
3. Keep `reason` plain text for runtime warnings.
4. Use `docs_reason` for docs-only markdown/xref text.
5. Prefer explicit replacement names in reasons.

### Field Pattern

```python
from typing import Annotated, Optional
from flet.utils.validation import V

old_prop: Annotated[
    Optional[str],
    V.deprecated(
        "new_prop",
        version="0.17.0",
        delete_version="0.18.0",
        reason="Use new_prop instead.",
        docs_reason="Use [`new_prop`][(c).] instead.",
    ),
] = None
```

### Function/Method Pattern

```python
from flet.utils.deprecated import deprecated

@deprecated(
    reason="Use new_func instead.",
    docs_reason="Use [`new_func()`][(m).new_func] instead.",
    version="0.17.0",
    delete_version="0.18.0",
)
def old_func():
    ...
```

### Class/Control Pattern

```python
from flet.utils.deprecated import deprecated_class

@deprecated_class(
    reason="Use NewControl instead.",
    docs_reason="Use [`NewControl`][flet.] instead.",
    version="0.17.0",
    delete_version="0.18.0",
)
class OldControl:
    ...
```

## `reason` vs `docs_reason`

- Runtime warnings always use `reason`.
- Docs admonitions prefer `docs_reason`; fallback is `reason`.
- Keep markdown/xref out of `reason` to avoid noisy runtime output.

For cross-reference shape rules, follow:
[`docs-cross-referencing`](../docs-cross-referencing/SKILL.md)

## Docs Behavior Expectations

For supported patterns, docs should auto-render:
- a `Deprecated` admonition section,
- a `deprecated` label/badge on the item.

Do not duplicate with manual deprecation admonitions in docstrings unless there
is a special case not covered by the extension.

## Required Test Matrix

When adding/changing deprecations, include tests for:
- runtime warning text (`reason`, versions, optional delete version),
- docs-only preference (`docs_reason` overrides `reason` in docs),
- docs rendering extraction for the used pattern (`V.deprecated`,
  `@deprecated`, `@deprecated_class`),
- label presence (`deprecated`) in docs extraction tests.

Prefer:
- `sdk/python/packages/flet/tests/test_deprecated.py`
- `sdk/python/packages/flet/tests/test_griffe_deprecations.py`
- `sdk/python/packages/flet/tests/test_validation.py` (for `V.deprecated`)

## Common Pitfalls

- Putting markdown/xref into runtime `reason`.
- Forgetting `delete_version` when a removal target is already known.
- Adding old/new value-copy logic in Python for rename migrations.
- Duplicating deprecation warnings in multiple lifecycle hooks manually.
- Broken crossref targets in `docs_reason` (for example malformed `[(c).]` links).
