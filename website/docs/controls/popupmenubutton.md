---
class_name: "flet.PopupMenuButton"
examples: "controls/material/popup_menu_button"
example_media: "examples/controls/material/popup_menu_button/media"
example_images: "test-images/examples/controls/material/golden/macos/popup_menu_button"
popup_menu_item_class_name: "flet.PopupMenuItem"
title: "PopupMenuButton"
---

import {ClassAll, ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Opened popup menu under button" imageWidth="11%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/popupmenubutton)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="35%" />

<ClassMembers name={frontMatter.class_name} />

<ClassAll name={frontMatter.popup_menu_item_class_name} />
