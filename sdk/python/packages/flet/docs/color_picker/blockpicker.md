---
class_name: flet_color_picker.BlockPicker
examples: ../../examples/controls/color_picker
example_images: ../test-images/examples/color_picker/golden/macos/color_picker_examples
---

# BlockPicker

Pick a color using a block picker from the `flet-color-picker` extension, which
wraps Flutter's [`flutter_colorpicker`](https://pub.dev/packages/flutter_colorpicker)
package.

{{ class_summary(class_name, example_images + "/block_picker.png", image_caption="Basic BlockPicker") }}

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
--8<-- "{{ examples }}/example_5.py"
```

## Description

{{ class_all_options(class_name) }}
