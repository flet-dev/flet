---
class_name: "flet.ExpansionTile"
examples: "controls/material/expansion_tile"
example_images: "test-images/examples/controls/material/golden/macos/expansion_tile"
title: "ExpansionTile"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic ExpansionTile" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansiontile)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} width="30%" />

### Programmatic expansion/collapse

<CodeExample path={frontMatter.examples + '/programmatic_expansion/main.py'} language="python" />

<Image src={frontMatter.example_images + '/programmatic_expansion_flow.gif'} width="50%" />

### Custom animations

<CodeExample path={frontMatter.examples + '/custom_animations/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_animations_default.gif'} width="50%" />

### Theme mode toggle

<CodeExample path={frontMatter.examples + '/theme_mode_toggle/main.py'} language="python" />

### Borders

<CodeExample path={frontMatter.examples + '/borders/main.py'} language="python" />

<Image src={frontMatter.example_images + '/borders_flow.gif'} width="50%" />

<ClassMembers name={frontMatter.class_name} />
