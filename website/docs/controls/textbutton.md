---
class_name: "flet.TextButton"
examples: "../../examples/controls/text_button"
example_images: "../test-images/examples/material/golden/macos/text_button"
title: "TextButton"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple text button" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/textbutton)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="55%" />

### Icons

<CodeExample path={frontMatter.examples + '/icons.py'} language="python" />

<Image src={frontMatter.example_images + '/icons.png'} alt="icons" width="55%" />

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_clicks.png'} alt="handling-clicks" width="55%" />

### Custom content

<CodeExample path={frontMatter.examples + '/custom_content.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_content.png'} alt="custom-content" width="55%" />

<ClassMembers name={frontMatter.class_name} />
