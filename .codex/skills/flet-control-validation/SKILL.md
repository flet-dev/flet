---
name: flet-control-validation
description: Use when adding or changing validation for Python controls in sdk/python/packages/, including Annotated/V rules, __validation_rules__, and property Raises docstrings.
---

## When To Use

Use this skill when you:
- add validation to a control property,
- migrate manual `before_update()` checks to `V` rules,
- update `Raises` sections tied to validation,
- align Python validation with Dart-side control behavior.

Do not use this skill for unrelated doc-only edits outside control validation.

## Source Of Truth

- Validation runtime API lives in:
  `sdk/python/packages/flet/src/flet/controls/validation.py`
- Import from public path only:
  `from flet.controls.validation import V`
  and when needed
  `from flet.controls.validation import ValidationRules`

## Validation Authoring Rules

1. Prefer field-level validation with `Annotated[...]` metadata.
   - Example:
     ```py
     value: Annotated[
               Optional[Number],
               V.ge_field("min"),
               V.le_field("max"),
           ] = None
     ```

2. Use class-level `__validation_rules__` only for invariants that cannot be expressed cleanly on one field.
   - Type:
     `__validation_rules__: ValidationRules = (...)`
   - Use `V.ensure(...)` with an explicit message for control-level invariants only when the lambda stays clear and readable.
   - If the lambda becomes hard to read, avoid `__validation_rules__` and implement that check in the `before_update()` override instead.

3. Keep the `before_update()` override for normalization/mutation and readability-first control checks.
   - Remove validation checks duplicated by `V` rules.
   - Prefer `before_update()` over `__validation_rules__` when it makes complex cross-field logic significantly clearer.

4. Cross-field comparisons use field rules only.
   - Use: `V.gt_field`, `V.ge_field`, `V.lt_field`, `V.le_field`

5. Match Dart effective behavior.
   - Check corresponding Flutter control.
   - If Dart applies defaults (for example `min`/`max`), Python should validate against the same effective defaults.
   - Add rules for wrapper-imposed constraints when relevant (for example, bounds/rounding/division constraints used in Dart formatting logic).

## Typing Style

- Follow the codebase typing style:
  - prefer `Optional[T]` over `T | None`,
  - use `Union[...]` when needed.

## Property Docstring Style

When a property has validation, document it in that property’s docstring (google style).

1. Add a `Raises:` block under the property docstring.

2. Use one `ValueError` entry per logical rule, except `between(...)`.
   - For `V.between(a, b)`, use one entry:
     `ValueError: If it is not between \`a\` and \`b\`, inclusive.`

3. Start each entry with `If it ...`, where 'it' refers to the property name.

4. Phrase entries as negations of the annotation rule:
   - `V.gt(x)` -> `If it is not strictly greater than \`x\`.`
   - `V.ge(x)` -> `If it is not greater than or equal to \`x\`.`
   - `V.lt(x)` -> `If it is not strictly less than \`x\`.`
   - `V.le(x)` -> `If it is not less than or equal to \`x\`.`
   - `V.ge_field("min")` -> `If it is not greater than or equal to [\`min\`][(c).].`
   - `V.le_field("max")` -> `If it is not less than or equal to [\`max\`][(c).].`
   - `V.visible_control()` -> `If it is not visible.`
   - `V.visible_controls(min_count=1)` -> `If it does not contain at least one visible Control.`
   - `V.visible_controls(min_count=n)` -> `If it does not contain at least \`n\` visible Controls.`
   - `V.str_or_visible_control()` -> `If it is neither a string nor a visible Control.`
   - `V.instance_of((A, B))` -> `If it is not of type \`A\` or \`B\`.`

5. Mention conditional applicability when needed.
   - Example:
     `..., when [\`value\`][(c).] is set.`

## Cross-Referencing Conventions

Follow the dedicated cross-reference guidance in:
[`docs-cross-referencing` skill](../docs-cross-referencing/SKILL.md).

Most common pattern to use in control property docstrings:
- same-class properties: `[\`prop\`][(c).]`

Keep symbol labels wrapped in backticks.

## Common Pitfalls

- Keeping stale manual `before_update()` validations after migration.
- Missing `Raises` entries on validated properties.
- Combining multiple non-between rules into one ambiguous `ValueError` sentence.
- Forgetting Dart defaults that still apply when Python property is omitted.
- Forcing complex `V.ensure(lambda ...)` expressions when `before_update()` would be cleaner.
