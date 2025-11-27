---
class_name: flet.ShaderMask
examples: ../../examples/controls/shader_mask
example_images: ../test-images/examples/core/golden/macos/shader_mask
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Linear gradient mask") }}

## Examples

### Pink glow around image edges

```python
--8<-- "{{ examples }}/pink_radial_glow.py"
```

{{ demo("shader_mask/pink_radial_glow", height="420", width="80%") }}

### Fade out bottom edge of an image

```python
--8<-- "{{ examples }}/fade_out_image_bottom.py"
```

{{ demo("shader_mask/fade_out_image_bottom", height="420", width="80%") }}

### Applying linear and radial gradients/shaders

```python
--8<-- "{{ examples }}/linear_and_radial_gradients.py"
```

{{ demo("shader_mask/linear_and_radial_gradients", height="420", width="80%") }}


{{ class_members(class_name) }}
