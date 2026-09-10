---
title: "Introduction"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {CodeExample, Image} from '@site/src/components/crocodocs';

Flet is a Python framework for building web, desktop, and mobile apps without prior experience in frontend development. Use ready-made controls to create your interface, connect your Python libraries and application logic, and handle user interactions without writing HTML, CSS, or JavaScript.

Start with a UI for a script or build a complete application with multiple screens. Develop with hot reload, try your app on your phone, and package it for Windows, macOS, Linux, iOS, or Android, or publish it to the web.

## Try Flet in your browser

[Flet Studio](/studio) lets you create and run Flet apps in your browser without installing anything. Write Python, customize a gallery example, or describe your idea to the AI agent and build from there.

This small counter app displays a number and increments it when you press **+**:

<CodeExample path="apps/templates/basic_counter/main.py" language="python" title="src/main.py" />

## Try Flet on your phone

Install the Flet app from the [App Store](https://apps.apple.com/app/flet/id1624979699) or [Google Play](https://play.google.com/store/apps/details?id=com.appveyor.flet) and explore its built-in **Gallery** to try controls and example apps on your device.

When you're ready to try your own code, [connect your phone to your development app](getting-started/testing-on-mobile.md) and see it refresh as you make changes.

## Try Flet on your desktop

To develop locally, [install Flet](getting-started/installation.md), [create a project](getting-started/create-flet-app.md), and [run it](getting-started/running-app.md). Your app opens in a desktop window and reloads when you save changes.

<Image src="assets/getting-started/counter-app/macos.png" alt="Counter app running on macOS" width="60%" />

:::tip[Quick desktop preview]
Already have [`uv`](https://docs.astral.sh/uv/#installation)? Run this in your terminal to open a minimal Flet app without creating a project:

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
