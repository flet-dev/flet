---
class_name: "flet.IconButton"
examples: "controls/material/icon_button"
example_images: "test-images/examples/controls/material/golden/macos/icon_button"
example_media: "examples/controls/material/icon_button/media"
title: "IconButton"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic IconButton" imageWidth="6%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/iconbutton)

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_clicks.gif'} alt="handling-clicks" width="40%" />

### Selected icon

<CodeExample path={frontMatter.examples + '/selected_icon/main.py'} language="python" />

<Image src={frontMatter.example_images + '/selected_icon.gif'} alt="selected-icon" width="20%" />

<ClassMembers name={frontMatter.class_name} />
