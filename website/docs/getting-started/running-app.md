---
title: "Running a Flet app (Hot Reload)"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {Image} from '@site/src/components/crocodocs';

Flet apps can be executed as either desktop or web applications using the [`flet run`](../cli/flet-run.md) command.
Doing so will start the app in a native OS window or a web browser, respectively, with hot reload enabled to view changes in real-time.

## Desktop app

To run Flet app as a desktop app, use the following command:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet run
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet run
```
</TabItem>
</Tabs>
When you run the command without any arguments, `main.py` script in the current directory will be executed, by default.

If you need to provide a different path, use the following command:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet run [script]
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet run [script]
```
</TabItem>
</Tabs>
Where `[script]` is a relative (ex: `counter.py`) or absolute (ex: `/Users/john/projects/flet-app/main.py`) path to the Python script you want to run.

The app will be started in a native OS window:

<div class="grid cards" markdown>

-   **macOS**

    ---
    <Image src="assets/getting-started/counter-app/macos.png" alt="macOS" width="65%" />

-   **Windows**

    ---
    <Image src="assets/getting-started/counter-app/windows.png" alt="windows" width="65%" />

</div>

## Web app

To run Flet app as a web app, use the `--web` (or `-w`) option:
<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet run --web [script]  # (1)!
```

1. A fixed port can be specified using `--port` ( or `-p`) option, followed by the port number.
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet run --web [script]  # (1)!
```

1. A fixed port can be specified using `--port` ( or `-p`) option, followed by the port number.
</TabItem>
</Tabs>
A new browser window/tab will be opened and the app will be using a random TCP port:

<Image src="assets/getting-started/counter-app/safari.png" alt="Web" width="45%" caption="Running Flet app as a web app" />

## Passing arguments to your app

Anything after a `--` separator is passed through to your app script instead of being
interpreted by Flet, and shows up there as `sys.argv[1:]`:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet run --web [script] -- --dataset big.csv --verbose
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet run --web [script] -- --dataset big.csv --verbose
```
</TabItem>
</Tabs>

Your app reads them as it would when started with `python`:

```python title="main.py"
import argparse
import sys

import flet as ft

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", default="small.csv")
parser.add_argument("--verbose", action="store_true")
options = parser.parse_args(sys.argv[1:])


def main(page: ft.Page):
    page.add(ft.Text(f"Dataset: {options.dataset}"))


ft.run(main)
```

The `--` separator is what keeps your app's arguments from being read as Flet's own -
without it, `flet run main.py --verbose` fails because `--verbose` is not a
[`flet run`](../cli/flet-run.md) option. Arguments that don't start with a `-` can be
passed without a separator, e.g. `flet run main.py big.csv`.

:::note
The same arguments are re-applied every time the app is hot reloaded, and they are
passed through in all run modes: desktop, `--web`, `--ios` and `--android`.
:::

## Watching for changes

By default, Flet will watch the script file that was run and reload the app whenever the contents
of this file are modified+saved, but will **not** watch for changes in other files.

To modify this behavior, you can use one or more of these [`flet run`](../cli/flet-run.md) options:

* `-d` or `--directory` to watch for changes in the `[script]`s directory only
* `-r` or `--recursive` to watch for changes in the `[script]`s directory and all sub-directories recursively

:::note[Example]

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet run --recursive [script]
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet run --recursive [script]
```
</TabItem>
</Tabs>
:::
