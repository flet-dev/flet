---
title: "Router"
class_name: flet.Router
examples: apps/router
---

import {ClassSummary, ClassMembers, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

`Router` matches the current page route against a tree of [Route](../types/route.md) definitions
and renders the matched component chain with nested outlet contexts.

Navigation is done via [page.navigate()](../controls/page.md#flet.Page.navigate) or [page.push_route()](../controls/page.md#flet.Page.push_route).

## Examples

### Basic

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

### Layout with outlet

<CodeExample path={frontMatter.examples + '/layout_outlet/main.py'} language="python" />

### Dynamic segments

<CodeExample path={frontMatter.examples + '/dynamic_segments/main.py'} language="python" />

### Loaders

<CodeExample path={frontMatter.examples + '/loaders/main.py'} language="python" />

### Active links

<CodeExample path={frontMatter.examples + '/active_links/main.py'} language="python" />

### Featured

<CodeExample path={frontMatter.examples + '/featured/main.py'} language="python" />

### Managed views — nested routes

Each route component returns a [View](../controls/view.md) with its own [AppBar](../controls/appbar.md).
Navigating deeper pushes views onto the stack; swipe-back and AppBar back button pop them.

<CodeExample path={frontMatter.examples + '/nested_routes/main.py'} language="python" />

### Managed views — shared layout with outlet

A layout route with `outlet=True` wraps child routes in a shared [View](../controls/view.md).
Leaf components return regular controls; the layout provides the View.

<CodeExample path={frontMatter.examples + '/nested_outlet_views/main.py'} language="python" />

### Managed views — full app with NavigationRail

Complete app with [NavigationRail](../controls/navigationrail.md), stacked project views,
and tabbed settings — all using `manage_views=True`.

<CodeExample path={frontMatter.examples + '/featured_views/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
