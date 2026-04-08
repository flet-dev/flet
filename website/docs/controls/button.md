---
class_name: "flet.Button"
examples: "controls/material/button"
example_images: "test-images/examples/material/golden/macos/button"
title: "Button"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Enabled and disabled buttons" imageWidth="25%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/elevatedbutton)

### Button

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="Basic button" width="25%" />

### Icons

<CodeExample path={frontMatter.examples + '/icons/main.py'} language="python" />

<Image src={frontMatter.example_images + '/icons.png'} alt="Basic button" width="35%" />

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_clicks.png'} alt="Handling clicks" width="35%" />

### Custom content

<CodeExample path={frontMatter.examples + '/custom_content/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_content.png'} alt="Buttons with custom content" width="35%" />

### Shapes

<CodeExample path={frontMatter.examples + '/button_shapes/main.py'} language="python" />

<Image src={frontMatter.example_images + '/button_shapes.png'} alt="Buttons with different shapes" width="35%" />

### Styling

<CodeExample path={frontMatter.examples + '/styling/main.py'} language="python" />

<Image src={frontMatter.example_images + '/styled_initial.png'} alt="Styled button - default state" width="25%" caption="Default state" />

<Image src={frontMatter.example_images + '/styled_hovered.png'} alt="Styled button - hovered state" width="25%" caption="Hovered state" />

### Animate on hover

<CodeExample path={frontMatter.examples + '/animate_on_hover/main.py'} language="python" />

<Image src={frontMatter.example_images + '/animate_on_hover_initial.png'} alt="Unhovered button" width="40%" caption="Normal button" />

<Image src={frontMatter.example_images + '/animate_on_hover_hovered.png'} alt="Hovered button" width="40%" caption="Hovered button" />

<ClassMembers name={frontMatter.class_name} />
