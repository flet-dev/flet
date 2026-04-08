---
class_name: "flet.CupertinoTextField"
examples: "controls/cupertino/cupertino_text_field"
example_images: "test-images/examples/cupertino/golden/macos/cupertino_textfield"
example_media: "examples/controls/cupertino/cupertino_text_field/media"
title: "CupertinoTextField"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic CupertinoTextField" imageWidth="40%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/cupertinotextfield)

### Basic Example

<CodeExample path={frontMatter.examples + '/cupertino_material_and_adaptive/main.py'} language="python" />

<Image src={frontMatter.example_media + '/cupertino_material_and_adaptive.png'} alt="cupertino-material-and-adaptive" width="70%" />

### Handling selection changes

<CodeExample path={frontMatter.examples + '/selection_change/main.py'} language="python" />

### Background image

<CodeExample path={frontMatter.examples + '/background_image/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
