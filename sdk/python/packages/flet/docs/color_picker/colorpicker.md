---
class_name: flet_color_picker.ColorPicker
examples: ../../examples/controls/color_picker
example_images: ../test-images/examples/color_picker/golden/macos/color_picker_examples
---

# ColorPicker

Pick a color using the `flet-color-picker` extension, which wraps Flutter's
[`flutter_colorpicker`](https://pub.dev/packages/flutter_colorpicker) package.

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic ColorPicker") }}

## Usage

Add `flet-color-picker` to your project dependencies:

/// tab | uv
```bash
uv add flet-color-picker
```

///
/// tab | pip
```bash
pip install flet-color-picker  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}
