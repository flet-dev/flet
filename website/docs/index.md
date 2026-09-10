---
title: "Introduction"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {CodeExample, Image} from '@site/src/components/crocodocs';

Flet is a framework that allows building web, desktop and mobile applications in Python without prior experience in frontend development.

Some features

What Flet can do what can't...

## Try Flet online

Before installing Flet on your computer you can try it online in your browser!

[Flet Studio](/studio) is ...

Below is a simple "Counter" app, with a text field and two buttons to increment and decrement the counter value:

<CodeExample path="apps/templates/basic_counter/main.py" language="python" title="src/main.py" />

## Try Flet on your phone

If you like to feel how Flet apps work/feel on a mobile device you can install Flet mobile app ([App Store](../), [Google Play](../)) and browse
its built-in Gallery.

[screenshot]

## Try Flet on your desktop

To run Flet app on your computer, [install](getting-started/installation.md) Flet, [create](/docs/getting-started/create-flet-app) a new project
and [run](/docs/getting-started/running-app) it.

This will open the app in a native OS window - what a nice alternative to Electron! 🙂

<p align="center">
    <img src="/docs/assets/getting-started/counter-app/macos.png" width="60%" />
</p>

:::note[Flet run one-liner]
If you have [`uv`](https://docs.astral.sh/uv/#installation) installed you can run this command to quickly try Flet on your desktop:

<Tabs>
<TabItem value="bash" label="Bash">

```bash
uvx --with flet-desktop -- python <<'PY'
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello from Flet!"))

ft.run(main)
PY
```

</TabItem>
<TabItem value="powershell" label="PowerShell">

```powershell
@'
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello from Flet!"))

ft.run(main)
'@ | uvx --with flet-desktop -- python -
```

</TabItem>
</Tabs>




:::
