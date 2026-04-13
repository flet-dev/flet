---
class_name: "flet.Dropdown"
examples: "controls/material/dropdown"
example_images: "test-images/examples/controls/material/golden/macos/dropdown"
example_media: "examples/controls/material/dropdown/media"
title: "Dropdown"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# Dropdown

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Dropdown" imageWidth="25%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Color selection with filtering

<CodeExample path={frontMatter.examples + '/color_selection_with_filtering/main.py'} language="python" />

<Image src={frontMatter.example_images + '/color_selection_with_filtering_flow.gif'} alt="color-selection-with-filtering" width="35%" />

### Icon selection

<CodeExample path={frontMatter.examples + '/icon_selection/main.py'} language="python" />

<Image src={frontMatter.example_images + '/icon_selection_flow.gif'} alt="icon-selection" width="35%" />

### Styled dropdowns

<CodeExample path={frontMatter.examples + '/styled/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
