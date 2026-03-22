---
class_name: "flet.Button"
examples: "../../examples/controls/button"
example_images: "../test-images/examples/material/golden/macos/button"
title: "Button"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Enabled and disabled buttons" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/elevatedbutton)

### Button

<CodeExample path={frontMatter.examples + '/basic.py'} />

<Image src={frontMatter.example_images + '/basic.png'} alt="Basic button" width="50%" />

### Icons

<CodeExample path={frontMatter.examples + '/icons.py'} />

<Image src={frontMatter.example_images + '/icons.png'} alt="Basic button" width="50%" />

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks.py'} />

<Image src={frontMatter.example_images + '/handling_clicks.png'} alt="Handling clicks" width="50%" />

### Custom content

<CodeExample path={frontMatter.examples + '/custom_content.py'} />

<Image src={frontMatter.example_images + '/custom_content.png'} alt="Buttons with custom content" width="50%" />

### Shapes

<CodeExample path={frontMatter.examples + '/button_shapes.py'} />

<Image src={frontMatter.example_images + '/button_shapes.png'} alt="Buttons with different shapes" width="50%" />

### Styling

<CodeExample path={frontMatter.examples + '/styling.py'} />

<Image src={frontMatter.example_images + '/styled_initial.png'} alt="Styled button - default state" width="50%" caption="Default state" />

<Image src={frontMatter.example_images + '/styled_hovered.png'} alt="Styled button - hovered state" width="50%" caption="Hovered state" />

### Animate on hover

<CodeExample path={frontMatter.examples + '/animate_on_hover.py'} />

<Image src={frontMatter.example_images + '/animate_on_hover_initial.png'} alt="Unhovered button" width="50%" caption="Normal button" />

<Image src={frontMatter.example_images + '/animate_on_hover_hovered.png'} alt="Hovered button" width="50%" caption="Hovered button" />

<ClassMembers name={frontMatter.class_name} />
