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

<CodeExample path={frontMatter.examples + '/routing/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/layout_outlet/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/dynamic_segments/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/loaders/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/active_links/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/featured/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/nested_routes/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/nested_outlet_views/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/featured_views/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/modal_routes/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/recursive_routes/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
