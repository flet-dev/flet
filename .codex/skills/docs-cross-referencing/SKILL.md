---
name: docs-cross-referencing
description: Documentation cross-reference conventions. Use when adding or editing docstrings under sdk/python/packages, fixing broken cross-links, or reviewing Python docstring links that should resolve through mkdocs python_xref.
---

## Instructions

Use these rules when writing or fixing cross-references in Python docstrings for SDK Python package docs.

1. Confirm scope and context
- Apply this skill to Python docstrings used by MkDocs in `sdk/python/packages`.
- Prefer cross-references to plain code formatting when referring to documented symbols.
- Apply these relative cross-reference rules only in Python docstrings. Markdown files must always use full explicit paths, for example, [`Page`][flet.Page].

2. Use python_xref target forms
- Use fully qualified targets when needed (usually, only in Markdown files): [`Page`][flet.Page], [`dataclass`][dataclasses.dataclass]. In Python docstrings, the short forms should be preferred, when possible.
- Use module-short targets when symbol is in that module: [`Page`][flet.], [`Tester`][flet.testing.], [`Arc`][flet.canvas.].
- Prefer `(c)` forms for same-class references: [`value`][(c).], [`that_method`][(c).that_method].
- `..` forms are valid and may be used, but are secondary: [`value`][..], [`that_method`][..].
- Use class/module/package shorthands for explicit targets: [`MyClass`][(c)], [`that_method`][(c).that_method], [`this module`][(m)], [`this package`][(p)].
- Use parent-scope shorthand when referencing a parent symbol: [`Color`][(p).color.].
- `^` forms are supported but not recommended: [`MyClass`][^], [`some_func`][^^.].
- Remember: if a target ends with `.`, the link title is appended to form the final path.

3. Keep link text and punctuation consistent
- Wrap the label in backticks for API symbols: [`Control`][flet.].
- Use single backticks for inline code and symbol names; never double-wrap inline code (for example, use `x`, not ``x``).
- Keep punctuation outside the link target unless it is part of the label text.
- Keep method call parentheses in the label when referring to calls: [`pick_files()`][(c).pick_files].
- Use `[(c).member]` when label has extra characters (for example `()`).
- If link-checking reports a known false-positive stdlib target, prefix the target with `?`, for example [`Path`][?pathlib.].

4. Prefer local shorthand
- Prefer [`Foo`][(c).] for same-class references instead of hardcoding full paths.
- Use [`Foo`][(c)] and [`bar`][(c).bar] when label and target differ or class-level clarity is needed.
- `[..]` is acceptable when it improves readability in local context.
- Prefer module-short targets when they are unambiguous in the package docs.
- Use fully-qualified paths when shorthand would be ambiguous.

5. Markdown files use full paths
- In Markdown docs (`.md`), do not rely on `python_xref` relative syntax (`(c)`, `(m)`, `(p)`, `^`, `..`).
- Use explicit full targets in Markdown links.

6. Preserve docstring style constraints while editing
- Keep Google-style docstrings and existing prose style.
- Keep lines wrapped with trailing `\` where needed to satisfy line-length formatting patterns already used in the file.

7. Validate quickly after edits
- Search modified files for markdown targets: `rg -n "\\[[^\\]]+\\]\\[[^\\]]+\\]" <files>`.
- Spot-check shorthand usage for `..`, `(c)`, `(m)`, `(p)`, and `^` forms.
- If `relative_crossrefs` and `check_crossrefs` are enabled, verify failures include source locations.
- Build docs or run the project doc checks if requested.

## Target cheat sheet

- Module-short:
  - [`Page`][flet.]
  - [`ControlState`][flet.]
- Explicit member path:
  - [`FilePicker.upload()`][flet.FilePicker.upload]
  - [`Page.route`][flet.Page.route]
- Submodule-short:
  - [`Tester`][flet.testing.]
  - [`Line`][flet.canvas.]
- Current class/enum shorthand (preferred):
  - [`value`][(c).]
  - [`upload()`][(c).upload]
- Current class/enum shorthand (also supported):
  - [`value`][..]
  - [`that_method`][..]
- Class/module/package:
  - [`MyClass`][(c)]
  - [`this module`][(m)]
  - [`this package`][(p)]
- Parent traversal:
  - [`MyClass`][^]
  - [`some_func`][^^.]
- Parent shorthand:
  - [`Color`][(p).color.]
- External inventory / non-package symbol:
  - [`dataclass`][dataclasses.dataclass]
  - [`Path`][?pathlib.] (use `?` only for known false-positive checks)

## Usage heuristics

1. Prefer `(c)` forms for members in the same type currently being documented.
2. Use `..` as an optional compact alternative when it improves readability.
3. Use package module-short targets (for example `flet.` or `flet.<submodule>.`) for symbols in stable modules.
4. Use full targets when shorthands are unclear to a reader/reviewer.
5. Keep symbol labels in backticks.
6. Keep prose readable first; links should clarify, not clutter.

## Common mistakes to avoid

- Plain text mention when a useful cross-reference exists.
- Defaulting to `..` when `(c)` would be clearer and more consistent in the file.
- Hardcoding long paths where local shorthand would stay correct through refactors.
- Mixing method label and target shape inconsistently, for example label with `()` but target without member.

## Cross-reference checking notes

- With `relative_crossrefs` enabled and `check_crossrefs` left at default (`true`), failures should include source locations.
- Use the `?` prefix only for known false positives (commonly some stdlib inventory lookups), not as a general bypass.

## Examples

```py
"""
Defines the file types that can be selected using the [`FilePicker`][flet.].
"""

"""
Called when a file is uploaded via [`upload()`][(c).upload] method.
"""

"""
Can be applied to any class including [`dataclass`][dataclasses.dataclass].
"""

"""
This function returns a [`Path`][?pathlib.] instance.
"""
```
