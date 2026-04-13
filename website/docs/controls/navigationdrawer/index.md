---
class_name: "flet.NavigationDrawer"
examples: "controls/navigation_drawer"
example_images: "test-images/examples/material/golden/macos/navigation_drawer"
title: "NavigationDrawer"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# NavigationDrawer

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Navigation drawer extended" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationdrawer)

### Start-aligned drawer

<CodeExample path={frontMatter.examples + '/position_start/main.py'} language="python" />

<Image src={frontMatter.example_images + '/position_start.gif'} alt="Start-aligned navigation drawer example" width="40%" />

### End-aligned drawer

<CodeExample path={frontMatter.examples + '/position_end/main.py'} language="python" />

<Image src={frontMatter.example_images + '/position_end.gif'} alt="End-aligned navigation drawer example" width="40%" />

### Theming

<CodeExample path={frontMatter.examples + '/theming/main.py'} language="python" />

<Image src={frontMatter.example_images + '/theming.gif'} alt="Themed navigation drawer example" width="40%" />

### Adaptive navigation

This example switches between a [`NavigationBar`](../navigationbar/index.md)
on narrow layouts and a [`NavigationRail`](../navigationrail/index.md) with an
end [`NavigationDrawer`](../navigationdrawer/index.md) on wider layouts.

<CodeExample path={frontMatter.examples + '/adaptive_navigation/main.py'} language="python" />

<Image src={frontMatter.example_images + '/adaptive_navigation.gif'} alt="Adaptive navigation example switching between a navigation bar and a navigation rail with an end drawer" width="55%" />

<ClassMembers name={frontMatter.class_name} />
