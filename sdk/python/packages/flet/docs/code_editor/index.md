---
class_name: flet_code_editor.CodeEditor
examples: ../../examples/controls/code_editor
---

# CodeEditor

Edit and highlight source code inside your [Flet](https://flet.dev) app using the `flet-code-editor` extension, which wraps Flutter's [`flutter_code_editor`](https://pub.dev/packages/flutter_code_editor) package.

## Usage

Add `flet-code-editor` to your project dependencies:

/// tab | uv
```bash
uv add flet-code-editor
```

///
/// tab | pip
```bash
pip install flet-code-editor  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}

### Named themes

You can pass a theme name (string) to `theme`, for example `"atom-one-light"`.

See also types:
- [`CodeTheme`](types/code_theme.md)
- [`GutterStyle`](types/gutter_style.md)
- [`TextEditingValue`](types/text_editing_value.md)
