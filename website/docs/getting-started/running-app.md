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
    <Image src="../assets/getting-started/counter-app/macos.png" alt="macOS" width="65%" />

-   **Windows**

    ---
    <Image src="../assets/getting-started/counter-app/windows.png" alt="windows" width="65%" />

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

<Image src="../assets/getting-started/counter-app/safari.png" alt="Web" width="45%" caption="Running Flet app as a web app" />

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
