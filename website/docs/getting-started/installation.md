---
title: "Installation"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

Flet is a Python library plus a command-line tool - [`flet create`](../cli/flet-create.md),
[`flet run`](../cli/flet-run.md), [`flet build`](../cli/flet-build.md),
[`flet test`](../cli/flet-test.md). What you have to install depends on the package manager you use:
with `uv`, nothing at all.

## Prerequisites

### Python version

Flet requires [Python](https://www.python.org/downloads/) 3.10 or later. Check the version you have
with `python --version`.

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

If you use the **light** flavor and need audio or video, you will need to install the required libraries yourself - see the [Audio](../services/audio/index.md#usage) and [Video](../controls/video/index.md#linux) setup guides.
</details>

<details>
<summary>Windows Subsystem for Linux (WSL)</summary>

Flet apps can be run on WSL 2 (Windows Subsystem for Linux 2).

However, if you are getting `cannot open display` error follow this
[guide](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg) for troubleshooting.
</details>

## Set up your package manager

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
[**uv**](https://docs.astral.sh/uv/) is "an extremely fast Python package and project manager,
written in Rust". [Install it](https://docs.astral.sh/uv/getting-started/installation/) if you
haven't already:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

That is the only thing you need to install - there is **no separate step to install Flet**, and no
virtual environment to create or activate by hand:

* [`uvx`](https://docs.astral.sh/uv/guides/tools/) runs the Flet CLI in a temporary, throwaway
  environment, which is all you need to scaffold a new app.
* Once the app exists, `uv run` installs its dependencies from the generated `pyproject.toml` into
  the project's own virtual environment.

Check that it works:

```bash
uvx --with flet-cli flet doctor
```

The `--with flet-cli` part is required: the `flet` package provides the `flet` command, but the
commands themselves live in the separate `flet-cli` package.

<details>
<summary>Optional: a global <code>flet</code> command</summary>

If you'd rather type `flet` than `uvx --with flet-cli flet`, install the CLI as a persistent
[uv tool](https://docs.astral.sh/uv/guides/tools/#installing-tools):

```bash
uv tool install --with flet-cli flet
flet doctor
```

Upgrade it with `uv tool upgrade flet`, and remove it with `uv tool uninstall flet`.

This is handy for commands that act on a project from the outside, such as `flet create`. To run or
build an app, prefer `uv run flet ...` from inside the project, so that the app uses its own pinned
dependencies rather than the global ones.
</details>
</TabItem>
<TabItem value="pip" label="pip">
pip has no equivalent of `uvx`, so Flet has to be installed into a
[virtual environment](https://docs.python.org/3/library/venv.html) that you create and activate
yourself.

Create a directory for your app, and a virtual environment inside it:

```bash
mkdir my-app
cd my-app
python -m venv .venv  # (1)!
source .venv/bin/activate  # (2)!
```

1. On Linux and macOS, use `python3 -m venv .venv` if `python` points to Python 2.x or isn't on your `PATH`.
2. On Windows, use `.venv\Scripts\activate` instead.

Then install Flet and check that it works:

```bash
pip install 'flet[all]'
flet doctor
```

Every `flet` command in these docs assumes this virtual environment is activated. You will need to
activate it again in each new terminal session.
</TabItem>
</Tabs>

## What gets installed

`flet[all]` is shorthand for the four packages that make up a complete Flet installation:

| Package | What it does |
| --- | --- |
| `flet` | The library you `import flet as ft`, and the `flet` command itself. |
| `flet-cli` | The implementation of `flet create`, `run`, `build`, `test` and the other [CLI commands](../cli/index.md). |
| `flet-desktop` | The desktop client that [`flet run`](running-app.md) opens your app in. |
| `flet-web` | The web client and server behind `flet run --web` and [`flet serve`](../cli/flet-serve.md). |

When you don't need all four, install them through individual extras instead: `flet[cli]`,
`flet[desktop]`, `flet[web]`, or `flet[test]` for the
[integration testing](integration-testing.md) dependencies. A bare `flet` gives you the library
only, which is what a deployed app usually needs.

:::note
If you run a `flet` command and `flet-cli` is missing from the current environment, Flet installs
the matching version for you before continuing. The same happens for `flet-desktop` and `flet-web`
the first time an app runs as a desktop or web app.
:::

## Adding Flet to an existing project

If you already have a project and just want Flet in it:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet
uv add --dev flet-cli flet-desktop flet-web 'flet[test]'
```

The first command makes `flet` a runtime dependency of your app. The second puts the tooling in the
`dev` dependency group, so it is available to `uv run flet ...` without shipping with your app. This
is the same layout that [`flet create`](../cli/flet-create.md) generates.
</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install 'flet[all]'
```

Unlike `uv add`, pip does not record anything: add `flet` to your `requirements.txt` or
`pyproject.toml` yourself.
</TabItem>
</Tabs>

## Installing a pre-release version

Flet publishes pre-release ("dev") builds to PyPI ahead of every stable release, so you can try out
upcoming changes early. They are listed on the
[release history page](https://pypi.org/project/flet/#history). Neither uv nor pip will install one
unless you ask for it.

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
Add `--prerelease allow` to any uv command:

```bash
# scaffold an app with the latest pre-release
uvx --prerelease allow --with flet-cli flet create my-app

# or pin an exact version
uvx --prerelease allow --from 'flet[cli]==1.1.0.dev5' flet create my-app

# a global CLI, or an existing project
uv tool install --prerelease allow --with flet-cli flet
uv add flet --prerelease allow
```

An app scaffolded by a pre-release CLI depends on a pre-release of Flet, so the flag is needed to
run it, too:

```bash
cd my-app
uv run --prerelease allow flet run
```

To stop repeating the flag, set it once in the app's `pyproject.toml`:

```toml
[tool.uv]
prerelease = "allow"
```
</TabItem>
<TabItem value="pip" label="pip">
Pass `--pre`, or pin an exact version:

```bash
pip install --pre 'flet[all]'

# or
pip install 'flet[all]==1.1.0.dev5'
```
</TabItem>
</Tabs>

## Upgrading Flet

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
# your app's dependencies
uv add flet --upgrade

# the global CLI, if you installed one
uv tool upgrade flet
```

`uvx` needs no upgrading - it picks up new releases on its own. Add `--refresh` if it looks like
it is using a stale cached version.
</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install 'flet[all]' --upgrade
```
</TabItem>
</Tabs>

## Next steps

Now you are ready to [create your first Flet app](create-flet-app.md).
