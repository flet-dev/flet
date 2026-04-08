---
class_name: "flet.AppBar"
examples: "controls/material/app_bar"
example_images: "test-images/examples/material/golden/macos/app_bar"
example_media: "examples/controls/material/app_bar/media"
title: "AppBar"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic AppBar" imageWidth="65%" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/appbar)

### Actions and Popup Menu

<CodeExample path={frontMatter.examples + '/actions_and_popup_menu/main.py'} language="python" />

<Image src={frontMatter.example_images + '/app_bar_flow.gif'} alt="actions-and-popup-menu" width="55%" />

### Theme and Material Mode Toggles

<CodeExample path={frontMatter.examples + '/theme_mode_toggle/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
