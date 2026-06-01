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

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/layout_outlet/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/dynamic_segments/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/loaders/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/active_links/main.py'} language="python" />

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

Complete app with [NavigationRail](../controls/navigationrail), stacked project views,
and tabbed settings — all using `manage_views=True`.

<CodeExample path={frontMatter.examples + '/featured_views/main.py'} language="python" />

### Modal routes

Routes marked `modal=True` are rendered as a fullscreen-dialog overlay on top
of the previous (non-modal) location's view stack. A *global* modal is declared
at the top level (the URL works from anywhere); a *local* modal is declared as
a child of a non-modal parent (the URL embeds the parent's segment, so
deep-link works without any state).

<CodeExample path={frontMatter.examples + '/modal_routes/main.py'} language="python" />

### Recursive routes

A route marked `recursive=True` can match itself as its own descendant — one
View is emitted per consumed URL segment. Use this for tree-shaped URLs
with unbounded depth (e.g. a file browser at `/folder/a/b/c`).

<CodeExample path={frontMatter.examples + '/recursive_routes/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
