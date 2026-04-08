---
class_name: "flet_rive.Rive"
examples: "extensions/rive"
title: "Rive"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Rive

Render [Rive](https://rive.app/) animations in your [Flet](https://flet.dev) app with the `flet-rive` extension.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅  (x64&nbsp;only) |  ✅  |    ✅    |  ✅  |

## Usage

Add `flet-rive` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-rive
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-rive  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
:::tip[Hosting Rive files]
Host `.riv` files locally or load them from a CDN. Use `placeholder` to keep layouts responsive while animations load.
:::

## Example

<CodeExample path={frontMatter.examples + '/example_1/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
