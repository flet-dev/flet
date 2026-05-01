---
class_name: "flet.ExpansionPanelList"
examples: "controls/material/expansion_panel_list"
example_images: "test-images/examples/controls/material/golden/macos/expansion_panel_list"
example_media: "examples/controls/material/expansion_panel_list/media"
title: "ExpansionPanelList"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic ExpansionPanelList" imageWidth="45%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansionpanellist)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic_flow.gif'} width="40%" />

### Scrolling

`ExpansionPanelList` supports scrolling through its [`scroll`](expansionpanellist.md) property.

<CodeExample path={frontMatter.examples + '/scrollable/main.py'} language="python" />

<Image src={frontMatter.example_images + '/scrollable.png'} width="40%" />

<ClassMembers name={frontMatter.class_name} />
