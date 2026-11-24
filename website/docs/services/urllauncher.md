---
class_name: "flet.UrlLauncher"
examples: "services/url_launcher"
title: "UrlLauncher"
---

import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

:::note[Opening a new tab in a web app]
A browser treats a new tab that was not opened during a click as a popup and
blocks it, so [`launch_url()`](urllauncher.md#flet.UrlLauncher.launch_url) with
`UrlTarget.BLANK` may not work on the web.

Set a control's `url` property, or use an
[`OpenUrl`](../types/openurl.md) action - both are performed by the client
inside the original gesture. See
[Client actions](../cookbook/client-actions.md).
:::

## Opening a URL with a client action

<CodeExample path={frontMatter.examples + '/open_url_action/main.py'} language="python" />

## Examples

<CodeExample path={frontMatter.examples + '/url_launcher/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
