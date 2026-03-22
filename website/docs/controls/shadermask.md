---
class_name: "flet.ShaderMask"
examples: "../../examples/controls/shader_mask"
example_images: "../test-images/examples/core/golden/macos/shader_mask"
title: "ShaderMask"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Linear gradient mask" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/shadermask)

### Pink glow around image edges

<CodeExample path={frontMatter.examples + '/pink_radial_glow.py'} />

<Image src={frontMatter.example_images + '/pink_radial_glow.png'} alt="pink-radial-glow" width="80%" />

### Fade out bottom edge of an image

<CodeExample path={frontMatter.examples + '/fade_out_image_bottom.py'} />

<Image src={frontMatter.example_images + '/fade_out_image_bottom.png'} alt="fade-out-image-bottom" width="80%" />

### Applying linear and radial gradients/shaders

<CodeExample path={frontMatter.examples + '/linear_and_radial_gradients.py'} />

<Image src={frontMatter.example_images + '/linear_and_radial_gradients.png'} alt="fade-out-image-bottom" width="80%" />

<ClassMembers name={frontMatter.class_name} />
