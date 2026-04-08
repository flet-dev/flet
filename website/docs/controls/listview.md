---
class_name: "flet.ListView"
examples: "controls/core/list_view"
example_media: "examples/controls/core/list_view/media"
example_images: "test-images/examples/core/golden/macos/list_view"
title: "ListView"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic list view" imageWidth="10%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/listview)

### Auto-scrolling and dynamical items addition

<CodeExample path={frontMatter.examples + '/autoscroll_and_dynamic_items/main.py'} language="python" />

<Image src={frontMatter.example_media + '/autoscroll_and_dynamic_items.gif'} alt="autoscroll-and-dynamic-items" width="40%" />

<ClassMembers name={frontMatter.class_name} />
