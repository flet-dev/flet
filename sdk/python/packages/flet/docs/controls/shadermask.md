---
class_name: flet.ShaderMask
examples: ../../examples/controls/shader_mask
example_images: ../test-images/examples/core/golden/macos/shader_mask
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Linear gradient mask") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/shadermask)

### Pink glow around image edges

```python
--8<-- "{{ examples }}/pink_radial_glow.py"
```

{{ image(example_images + "/pink_radial_glow.png", alt="pink-radial-glow", width="80%") }}



### Fade out bottom edge of an image

```python
--8<-- "{{ examples }}/fade_out_image_bottom.py"
```

{{ image(example_images + "/fade_out_image_bottom.png", alt="fade-out-image-bottom", width="80%") }}


### Applying linear and radial gradients/shaders

```python
--8<-- "{{ examples }}/linear_and_radial_gradients.py"
```

{{ class_members(class_name) }}
