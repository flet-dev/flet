
/// details | Prerequisites
    open: True
### Python version

Flet requires [Python](https://www.python.org/downloads/) 3.10 or later. (1)
{ .annotate }

1. Check your Python version using `python --version`.

### Operating System

#### macOS

Flet supports macOS 11 (Big Sur) or later.

#### Windows

Flet supports 64-bit version of Microsoft Windows 10 or later.

#### Linux

Flet supports Debian Linux 11 or later and Ubuntu Linux 20.04 LTS or later.

/// details | Windows Subsystem for Linux (WSL)
    type: note

Flet apps can be run on WSL 2 (Windows Subsystem for Linux 2).

However, if you are getting `cannot open display` error follow this
[guide](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg) for troubleshooting.
///

///

##  Creating a virtual environment (venv)

We recommend using a virtual environment for your Flet projects to keep dependencies
isolated and avoid conflicts with your other Python projects.

First, create a new directory for your Flet project and switch into it:

```bash
mkdir my-app
cd my-app
```

Next, create and activate a virtual environment (we recommend using `uv` as package manager):

/// tab | uv
[**uv**](https://docs.astral.sh/uv/) is "An extremely fast Python package and project manager, written in Rust".

[Install `uv`](https://docs.astral.sh/uv/getting-started/installation) if you haven't already, then run the following commands:

```bash
uv init --python='>=3.10'
uv venv
source .venv/bin/activate # (1)!
```

1. If you are on Windows, use `.venv\Scripts\activate` instead.
///
/// tab | pip
Using Python's built-in [`venv`](https://docs.python.org/3/library/venv.html) module:
```bash
python -m venv .venv  # (1)!
source .venv/bin/activate # (2)!
```

1. On Unix-like systems (Linux, macOS), use `python3 -m venv .venv` if `python` points to Python 2.x.
2. If you are on Windows, use `.venv\Scripts\activate` instead.
///
/// tab | poetry
[Poetry](https://python-poetry.org/docs/) is a Python dependency manager and package manager.

[Install Poetry](https://python-poetry.org/docs/#installation) if you haven't already, then run the following commands:

```bash
poetry init --python='>=3.10' --no-interaction
```
///

## Install Flet

To install Flet and add it to your project dependencies,
do the following depending on your package manager:

/// tab | uv
```bash
uv add 'flet[all]'
```
///
/// tab | pip
```bash
pip install 'flet[all]' # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///
/// tab | poetry
```bash
poetry add 'flet[all]'
```
///

## Verify installation

To make sure Flet has been installed correctly, we can check its version using the `--version` (or `-V`) flag or the [`doctor`](../cli/doctor.md) command:

/// tab | uv
```bash
uv run flet --version
# or
uv run flet doctor
```
///
/// tab | pip
```bash
flet --version
# or
flet doctor
```
///
/// tab | poetry
```bash
poetry run flet --version
# or
poetry run flet doctor
```
///

Now you are ready to [create your first Flet app](create-flet-app.md).

## Upgrade Flet

To upgrade Flet to the latest version, use the `--upgrade` flag:

/// tab | uv
```bash
uv add 'flet[all]' --upgrade
```
///
/// tab | pip
```bash
pip install 'flet[all]' --upgrade
```
///
/// tab | poetry
```bash
poetry add flet[all]@latest
```
///
