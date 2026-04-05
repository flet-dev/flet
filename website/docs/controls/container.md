---
class_name: "flet.Container"
examples: "controls/container"
example_media: "examples/controls/container/media"
example_images: "test-images/examples/core/golden/macos/container"
title: "Container"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_media + '/overview_padding_margin_border.png'} imageCaption="Container explained" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/container)

### Clickable container

<CodeExample path={frontMatter.examples + '/clickable/main.py'} language="python" />

<Image src={frontMatter.example_media + '/clickable.gif'} width="65%" />

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks/main.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_clicks.gif'} width="40%" />

### Handling hovers

<CodeExample path={frontMatter.examples + '/handling_hovers/main.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_hovers.gif'} width="15%" />

### Animate 1

<CodeExample path={frontMatter.examples + '/animate_1/main.py'} language="python" />

<Image src={frontMatter.example_media + '/animate_1.gif'} width="25%" />

### Animate 2

<CodeExample path={frontMatter.examples + '/animate_2/main.py'} language="python" />

### Animate 3

<CodeExample path={frontMatter.examples + '/animate_3/main.py'} language="python" />

### Nested themes 1

<CodeExample path={frontMatter.examples + '/nested_themes_1/main.py'} language="python" />

<Image src={frontMatter.example_images + '/nested_themes_1.png'} width="40%" />

### Nested themes 2

<CodeExample path={frontMatter.examples + '/nested_themes_2/main.py'} language="python" />

<Image src={frontMatter.example_images + '/nested_themes_2.png'} width="60%" />

### Nested themes 3

<CodeExample path={frontMatter.examples + '/nested_themes_3/main.py'} language="python" />

<Image src={frontMatter.example_media + '/nested_themes_3.gif'} width="40%" />

### Size aware

<CodeExample path={frontMatter.examples + '/size_aware/main.py'} language="python" />

<Image src={frontMatter.example_images + '/size_aware.png'} width="40%" />

<ClassMembers name={frontMatter.class_name} />
