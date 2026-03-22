---
title: "Installation"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

## Prerequisites

### Python version

Flet requires [Python](https://www.python.org/downloads/) 3.10 or later. (1)

1. Check your Python version using `python --version`.

### Operating System

#### macOS

Flet supports macOS 12 (Monterey) or later.

#### Windows

Flet supports 64-bit version of Microsoft Windows 10 and Windows 11.

#### Linux

Flet supports Debian 10, 11 and 12 and Ubuntu 20.04, 22.04 and 24.04 LTS.

<details>
<summary>Desktop flavor (audio & video support)</summary>

On Linux, the Flet desktop client is available in two flavors: **full** and **light**.

The **light** flavor (default on Linux) does not include audio and video extensions, resulting in a smaller download. The **full** flavor bundles audio and video support out of the box.

To select the flavor, either set the `FLET_DESKTOP_FLAVOR` environment variable:

```bash
export FLET_DESKTOP_FLAVOR=full
```

or add the setting to your project's `pyproject.toml`:

```toml
[tool.flet]
desktop_flavor = "full"
```

If you use the **light** flavor and need audio or video, you will need to install the required libraries yourself — see the [Audio](../audio/index.md#linux-requirements) and [Video](../video/index.md#linux) setup guides.
</details>

<details>
<summary>Windows Subsystem for Linux (WSL)</summary>

Flet apps can be run on WSL 2 (Windows Subsystem for Linux 2).

However, if you are getting `cannot open display` error follow this
[guide](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg) for troubleshooting.
</details>

##  Creating a virtual environment (venv)

We recommend using a virtual environment for your Flet projects to keep dependencies
isolated and avoid conflicts with your other Python projects.

First, create a new directory for your Flet project and switch into it:

```bash
mkdir my-app
cd my-app
```

Next, create and activate a virtual environment (we recommend using `uv` as package manager):

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
[**uv**](https://docs.astral.sh/uv/) is "An extremely fast Python package and project manager, written in Rust".

[Install `uv`](https://docs.astral.sh/uv/getting-started/installation) if you haven't already, then run the following commands:

```bash
uv init --python='>=3.10'
uv venv
source .venv/bin/activate # (1)!
```

1. If you are on Windows, use `.venv\Scripts\activate` instead.
</TabItem>
<TabItem value="pip" label="pip">
Using Python's built-in [`venv`](https://docs.python.org/3/library/venv.html) module:
```bash
python -m venv .venv  # (1)!
source .venv/bin/activate # (2)!
```

1. On Unix-like systems (Linux, macOS), use `python3 -m venv .venv` if `python` points to Python 2.x.
2. If you are on Windows, use `.venv\Scripts\activate` instead.
</TabItem>
</Tabs>
## Install Flet

To install Flet and add it to your project dependencies,
do the following depending on your package manager:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add 'flet[all]'
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install 'flet[all]' # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Verify installation

To make sure Flet has been installed correctly, we can check its version using the `--version` (or `-V`) flag or the [`doctor`](../cli/flet-doctor.md) command:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet --version
# or
uv run flet doctor
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet --version
# or
flet doctor
```
</TabItem>
</Tabs>
Now you are ready to [create your first Flet app](create-flet-app.md).

## Upgrade Flet

To upgrade Flet to its latest version:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add 'flet[all]' --upgrade
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install 'flet[all]' --upgrade
```
</TabItem>
</Tabs>
