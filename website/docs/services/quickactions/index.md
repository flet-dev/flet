---
class_name: "flet_quick_actions.QuickActions"
examples: "extensions/quick-actions"
title: "Quick Actions"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

Manage the app's home-screen quick actions (the shortcuts that appear when the
user long-presses the app icon) in your [Flet](https://flet.dev) app via the
`flet-quick-actions` extension, built on top of Flutter's
[`quick_actions`](https://pub.dev/packages/quick_actions) package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

Quick actions are a mobile-only OS feature. On other platforms every method
raises an exception and the `on_action` event never fires.

## Usage

Add `flet-quick-actions` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-quick-actions```
</TabItem> 

<TabItem value="pip" label="pip"> 
```bash
pip install flet-quick-actions # (1)! ```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

## Example

<CodeExample path={frontMatter.examples + '/quick-actions/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />