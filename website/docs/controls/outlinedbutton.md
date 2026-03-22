---
class_name: "flet.OutlinedButton"
examples: "../../examples/controls/outlined_button"
example_media: "../examples/controls/outlined_button/media"
example_images: "../test-images/examples/material/golden/macos/outlined_button"
title: "OutlinedButton"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple Outlined Button" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/outlinedbutton)

### Basic example

<CodeExample path={frontMatter.examples + '/basic.py'} />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="80%" />

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks.py'} />

<Image src={frontMatter.example_images + '/handling_clicks.gif'} alt="handling-clicks" width="80%" />

### Icons

<CodeExample path={frontMatter.examples + '/icons.py'} />

<Image src={frontMatter.example_images + '/icons.png'} alt="icons" width="80%" />

### Custom content

<CodeExample path={frontMatter.examples + '/custom_content.py'} />

<Image src={frontMatter.example_images + '/custom_content.png'} alt="custom-content" width="80%" />

<ClassMembers name={frontMatter.class_name} />
