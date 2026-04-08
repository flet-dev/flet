---
class_name: "flet.NavigationBar"
examples: "controls/navigation_bar"
example_images: "test-images/examples/material/golden/macos/navigation_bar"
title: "NavigationBar"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# NavigationBar

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple navigation bar" imageWidth="35%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationbar)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="40%" />

### Adaptive navigation

This example switches between a `NavigationBar`
on narrow layouts and a [`NavigationRail`](../navigationrail/index.md) with an
end [`NavigationDrawer`](../navigationdrawer/index.md) on wider layouts.

<CodeExample path={'controls/navigation_drawer/adaptive_navigation/main.py'} language="python" />

<Image src={'test-images/examples/material/golden/macos/navigation_drawer/adaptive_navigation.gif'} alt="Adaptive navigation example switching between a navigation bar and a navigation rail with an end drawer" width="55%" />

<ClassMembers name={frontMatter.class_name} />
