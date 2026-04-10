---
name: flet-validation
description: Use when adding or changing validation for Python controls (dataclasses) in sdk/python/packages/, including Annotated/V rules, __validation_rules__, and property Raises docstrings.
---

## When To Use

Use this skill when you:
- add validation to a control property,
- migrate manual `before_update()` checks to `V` rules,
- update `Raises` sections tied to validation,
- align Python validation with Dart-side control behavior.

Do not use this skill for unrelated doc-only edits outside control validation.
Do not use this skill for deprecation authoring conventions; use
[`flet-deprecation`](../flet-deprecation/SKILL.md).

## Source Of Truth

- Validation runtime API lives in:
  `sdk/python/packages/flet/src/flet/utils/validation.py`
- The same runtime can validate regular dataclass models via `validate(instance)`;
  this skill focuses on the control-specific authoring conventions.
- Import from public path only:
  `from flet.utils.validation import V`
  and when needed
  `from flet.utils.validation import ValidationRules`

## Validation Decision Order

Use this order and stop at the first option that keeps logic clear:
1. `Annotated[..., V.*]` field rules (default).
2. `__validation_rules__: ValidationRules` for cross-field invariants that do
   not map cleanly to one field.
3. `before_update()` only for normalization/mutation, or for truly non-ruleable
   invariants.

Never duplicate the same invariant in more than one layer.

## Validation Authoring Rules

1. Prefer field-level validation with `Annotated[...]` metadata.
   - Example (close to current slider controls):
     ```
     @dataclass
     class Sample:
         opacity: Annotated[
                Optional[Number],
                V.between(0.0, 1.0),
            ] = None

         value: Annotated[
             Optional[Number],
             V.ge_field("min"),
             V.le_field("max"),
         ] = None

         min: Annotated[
             Number,
             V.le_field("max"),
             V.le_field("value"),
         ] = 0.0

         max: Annotated[
             Number,
             V.ge_field("min"),
             V.ge_field("value"),
         ] = 1.0
     ```

2. Use class-level `__validation_rules__` only for invariants that cannot be
   expressed cleanly with field rules.
   - Type:
     `__validation_rules__: ValidationRules = (...)`
   - Use `V.ensure(...)` with an explicit message only when the predicate is
     short and readable.
   - If `V.ensure(lambda ...)` becomes hard to read, prefer either:
     1. a named predicate function passed to `V.ensure(...)`, or
     2. a clear `before_update()` check when it cannot be represented well with
        existing `V.*` rules.

3. Keep the `before_update()` override for normalization/mutation first.
   - Remove validation checks duplicated by `V` rules.
   - Prefer raising validation errors from rule evaluation (`validate()`), not
     from ad-hoc `before_update()` checks, unless the invariant is genuinely
     non-ruleable with current validation primitives.

4. Cross-field comparisons use field rules only.
   - Use: `V.gt_field`, `V.ge_field`, `V.lt_field`, `V.le_field`

5. `None` handling is inferred from type hints.
   - If a field is annotated as optional (for example `Optional[T]`), `None` is allowed.
   - If a field is not optional, `None` fails validation.
   - For `*_field` comparisons, if either side is optional and currently `None`, the
     comparison is skipped; if a non-optional side is `None`, validation fails.

6. Match Dart effective behavior.
   - Review both:
     1. Flet Dart wrapper (`packages/flet/lib/src/controls/<control>.dart` or
        extension wrapper),
     2. wrapped Flutter widget source assertions/invariants.
   - Mirror those constraints in Python so invalid payloads fail before crossing
     to Dart.
   - Validate against effective defaults applied on Dart side (for example
     `min`/`max`).
   - Include wrapper-imposed constraints when relevant (for example
     bounds/rounding/division logic in wrapper formatting code).

7. For new properties, validate against base widget assertions before wiring.
   - When adding a Python property to a Flet control, confirm whether the mapped
     Dart wrapper and underlying widget both enforce constraints for that property.
   - Add equivalent Python-side validation (`Annotated[...]`, `__validation_rules__`,
     or readable `before_update()`) to prevent Dart assertions from being the first
     failure point.

8. Keep error ownership clear.
   - Runtime outbound value failures should raise `ValueError`.
   - Validation declaration/build errors (invalid `V.*` arguments) should raise
     `ValidationDeclarationError`.

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

4. Use canonical wording from validation helper docstrings.
   - The source of truth is
     `sdk/python/packages/flet/src/flet/utils/validation.py`.
   - Each `V.*` helper includes `Property docstring Raises wording`.
   - Keep property `Raises` entries as negations of the annotation rule.
   - For strict inequalities, say `"strictly"`.
     For example: `V.gt(x)` -> `ValueError: If it is not strictly greater than \`x\`.`
   - For sign-neutral divisibility helpers (`factor_of`, `multiple_of`), add
     explicit sign rules (`V.gt(0)` or `V.lt(0)`) when direction matters, and
     include separate `Raises` entries for those sign rules.

5. Mention conditional applicability when needed.
   - Example (for `min`/`max` checks against optional `value`):
     ```
     Raises:
         ValueError: If it is not less than or equal to [`value`][(c).],
             when [`value`][(c).] is set.
     ```

6. Keep examples and wording aligned with real control files.
   - Prefer concrete property names such as `min`, `max`, `value`,
     `start_value`, `end_value`, `min_lines`, `max_lines`.
   - For cross-field rules, use same-class links: [`min`][(c).], [`max`][(c).].

## Cross-Referencing Conventions

Follow the dedicated cross-reference guidance in:
[`docs-cross-referencing` skill](../docs-cross-referencing/SKILL.md).

Most common pattern to use in control property docstrings:
- same-class properties: `[\`prop\`][(c).]`

Keep symbol labels wrapped in backticks.

## Required Test Matrix

When adding/changing validation, include tests that cover:
- one valid case and one invalid case per new logical rule;
- boundary values (`==`, min/max edges) where applicable;
- cross-field set/unset combinations when optional values are involved;
- effective-default behavior when Dart applies defaults but Python value is
  omitted.

Prefer placing tests in:
- `sdk/python/packages/flet/tests/test_validation.py` for validation runtime;
- control-specific tests when behavior is tied to one control.

## Common Pitfalls

- Keeping stale manual `before_update()` validations after migration.
- Missing `Raises` entries on validated properties.
- Combining multiple non-between rules into one ambiguous `ValueError` sentence.
- Forgetting Dart defaults that still apply when Python property is omitted.
- Forcing complex `V.ensure(lambda ...)` expressions when `before_update()` would be cleaner.
