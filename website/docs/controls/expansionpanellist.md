---
class_name: "flet.ExpansionPanelList"
examples: "controls/expansion_panel_list"
example_images: "../test-images/examples/material/golden/macos/expansion_panel_list"
example_media: "../examples/controls/expansion_panel_list/media"
title: "ExpansionPanelList"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic ExpansionPanelList" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansionpanellist)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} width="55%" />

### Scrolling

`ExpansionPanelList` supports scrolling through its [`scroll`](expansionpanellist.md) property.

<CodeExample path={frontMatter.examples + '/scrollable.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
