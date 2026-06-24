# Contributing to Flet

Thank you for your interest in contributing to Flet!

## Contents

- [Clone repo](#clone-repo)
- [Python SDK](#python-sdk)
  - [Install uv](#install-uv)
  - [Open worker directory](#open-worker-directory)
  - [Install dependencies](#install-dependencies)
  - [Check the installation](#check-the-installation)
  - [Running tests](#running-tests)
  - [Code formatting](#code-formatting)
  - [pre-commit](#pre-commit)
- [Flutter client](#flutter-client)
  - [Building the Flutter client](#building-the-flutter-client)
  - [Running the Flutter client](#running-the-flutter-client)
  - [Restarting/Rebuilding](#restartingrebuilding)
- [Development & Release Workflow](#development--release-workflow)
  - [Branching strategy](#branching-strategy)
  - [Contributor guidelines](#contributor-guidelines)
  - [Starting a release cycle](#starting-a-release-cycle)
  - [Publishing a pre-release](#publishing-a-pre-release)
  - [Publishing a stable release](#publishing-a-stable-release)
  - [Hotfixes](#hotfixes)
  - [Release preparation steps](#release-preparation-steps)
- [New macOS environment for Flet developer](#new-macos-environment-for-flet-developer)

## Clone repo

```
git clone https://github.com/flet-dev/flet
```

## Python SDK

### Install uv

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Be sure to add `%USERPROFILE%\AppData\Roaming\Python\Scripts` to `PATH`.

#### macOS/Linux

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Open worker directory

```
cd sdk/python
```

### Install dependencies

To install all Flet dependencies and enable the project as editable package run:

```
uv sync
```

### Check the installation

Create `hello.py` file with a minimal Flet program:

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello, world!"))

ft.run(main)
```

and then run it:

```
uv run python hello.py
```

During the first run Flet Client (`flet`) executable will be downloaded from [Flet GitHub releases](https://github.com/flet-dev/flet/releases) to a user temp directory and then started from there. The version of release to download from is taken from `flet/version.py` file.

You should see a new native OS window opened with "Hello, world!" in it.

### Running tests

Pytest should be run with `uv run`:

```
uv run pytest
```

For details on running and updating integration tests (including golden images),
see [integration tests README](sdk/python/packages/flet/integration_tests/README.md).

### Code formatting

The project uses [Black](https://github.com/psf/black) formatting style. All `.py` files in a PR must be black-formatted.

Install `black` extension for Visualtudio Code: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

IDE-specific Black integration guides:

- [VSCode: Using Black to automatically format Python](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0)
- [Formatting Python in VS Code](https://code.visualstudio.com/docs/python/formatting)

#### Type checking

Enable "pylance" type checking in VS Code.

Open user settings, search by "pylance", scroll down to **Python > Analysis: Type checking mode** section. Enable _basic_ mode.

#### Sort imports on Save

Install `isort` extension for imports formatting: https://marketplace.visualstudio.com/items?itemName=ms-python.isort

### pre-commit

[pre-commit](https://pre-commit.com) is a dev dependency of Flet and is automatically installed by `uv sync`.
To install the pre-commit hooks run: `uv run pre-commit install`.
Once installed, every time you commit, pre-commit will run the configured hooks against changed files.

## Flutter client

Add the `FLET_VIEW_PATH` and `FLET_WEB_PATH` variables to the environment variables or profile scripts for your respective OS, making sure to modify the path accordingly:

- On macOS (in `~/.zprofile` or any other profile script)*:
```
# Flet
export FLET_VIEW_PATH="$HOME/{path-to-flet}/flet/client/build/macos/Build/Products/Release"
export FLET_WEB_PATH="$HOME/{path-to-flet}/flet/client/build/web"
```


- On Windows (open "System Properties" > "Environment Variables", then add a new environment variable):
  - as "Variable name", enter `FLET_VIEW_PATH`, and as "Value", `{path-to-flet}\flet\client\build\windows\x64\runner\Release`
  - as "Variable name", enter `FLET_WEB_PATH`, and as "Value", `{path-to-flet}\flet\client\build\web`

- On Linux (in `~/.bash_profile` or any other profile script)*:
```
# Flet
export FLET_VIEW_PATH="$HOME/{path-to-flet}/flet/client/build/linux/{arch}/release/bundle"
export FLET_WEB_PATH="$HOME/{path-to-flet}/flet/client/build/web"
```


If you have Microsoft Edge installed and want to use it for debugging Flutter apps:

```
# Flutter
export CHROME_EXECUTABLE="/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
```

If you added these through the terminal, close that terminal session and create a new one.

\* <small>if continuing in the same shell run `source ~/.zprofile` to activate variables in current session</small>

### Building the Flutter client
Open an instance of your IDE (preferably VS Code) at the `flet-dev/flet/client` directory.

First, run `printenv | grep FLET` (or `gci env:* | findstr FLET` on Windows) in the built-in terminal to make sure everything is set. You should see the above environment variables you set (`FLET_VIEW_PATH`, `FLET_WEB_PATH`) printed out.

-  To build the Flutter client for MacOS, run:
    ```
    fvm flutter build macos
    ```
    When the build is complete, you should see the Flet bundle in the `FLET_VIEW_PATH`. (Running it will open a blank window.)
-  To build the Flutter client for Web, run the below command:
    ```
    fvm flutter build web --wasm
    ```
    When the build is complete, a directory `client/build/web` will be created.

### Running the Flutter client
Now open another instance of VS Code at `flet-dev/flet/sdk/python` directory.

Create a new folder preferably named `playground` (it has been added to the gitignore) in which you will test your additions.

Try running the below command, where `<your-main.py>` is the file to test your additions:

```bash
uv run flet run -w -p 8550 playground/<your-main.py>
```
You should see http://127.0.0.1:8550/ opened in the browser and also a desktop window with the output of your code.
Making changes to the `<your-main.py>` will automatically trigger a hot reload.

Now, switch to your flutter vscode instance and run the below command to start/connect the flet client:
```bash
flutter run
```
then choose your device from the shown options.
You will be able to see the debugging outputs of the flet client in this terminal.

### Restarting/Rebuilding

- When you make changes to the flet **dart** files, you will need to restart/rerun the Flutter client for the changes to take effect in your playground. There are two ways to do this:
  - fastest: press the keyboard button `R` while in the client's terminal (press `h` to see all other possible options);
  - slowest: use `flutter run` as seen previously.

- When you make changes to the flet **python** files, you will need to restart/rerun the Python client for the changes to take effect in the opened flutter applications. This is done with the same command:

```bash
uv run flet run -w -p 8550 playground/<your-main.py>
```

## Development & Release Workflow

### Branching strategy

* **`main`** — always contains the latest stable release. Protected branch.
* **`release/v{version}`** — integration branch for the next release, for example `release/v0.85.0`. Created from `main` at the start of a release cycle.
* **`feature/*`**, **`fix/*`** — short-lived branches created from the release branch and merged back into it via PR.

### Contributor guidelines

* Target your PRs to the active `release/v{version}` branch (not `main`).
* Add a new changelog record to the active release section in the root `CHANGELOG.md` in every PR targeting `release/v{version}`.
* Assign the release milestone to all related issues and PRs.

### Starting a release cycle

1. Create a new GitHub milestone for the version (e.g., `0.85.0`).
2. Create a `release/v{version}` branch from `main`.
3. Update package version to `{version}` in `packages/flet/pubspec.yaml`.
4. Add `## {version}` into `CHANGELOG.md` and `packages/flet/CHANGELOG.md`.
5. Require every PR targeting `release/v{version}` to append a new record to the active root changelog section.

### Publishing a pre-release

1. On the release branch, create and push a tag with the format `vX.Y.Z.devN` (start from `dev0`, e.g., `v0.85.0.dev0`).
2. CI builds and runs all tests. If everything passes, it creates a pre-release GitHub Release and publishes pre-release packages to PyPI. Pre-releases are **not** published to pub.dev.
3. Increment `N` for each subsequent pre-release (`dev1`, `dev2`, ...).

### Publishing a stable release

1. Prepare the release on the release branch (see [Release preparation steps](#release-preparation-steps) below).
2. Create `Flet {version}` PR from `release/v{version}` into `main`.
3. Merge into `main` using a **regular merge** (not squash).
4. Create and push a `v{version}` tag on `main` (e.g., `v0.85.0`).
5. CI publishes to PyPI, pub.dev, and creates a GitHub Release.
6. Close the milestone — mark remaining issues as fixed.
7. Delete the `release/v{version}` branch.
8. Clean up pre-release GitHub Releases and pre-release versions on PyPI.

### Hotfixes

For patches to the current stable release, branch directly from `main`, fix, open a PR back to `main`, merge and tag.

### Release preparation steps

* Keep the `## {version}` section in `packages/flet/CHANGELOG.md` in sync with the root `CHANGELOG.md` before tagging the release.
* Ensure every merged PR on `release/v{version}` added a new record to the active root `CHANGELOG.md` section.
* Open terminal in `client` directory and run `flutter pub get` to update Flet dependency versions in `client/pubspec.lock`.
* Templates are in `sdk/python/templates/` and automatically packaged as zip artifacts with the GitHub Release. No manual branch creation in external repos is needed.
* The supported Python / Pyodide versions are loaded on demand from [python-build's](https://github.com/flet-dev/python-build) date-keyed `manifest.json`; flet pins one release via `PYTHON_BUILD_RELEASE_DATE` in `sdk/python/packages/flet-cli/src/flet_cli/utils/python_versions.py`. When bumping it, keep it aligned with serious_python's `pythonReleaseDate` (both should track the same python-build release).

## New macOS environment for Flet developer

This section outlines how to prepare a fresh macOS environment for Flet development.

### Prerequisites

* **uv**: https://docs.astral.sh/uv/getting-started/installation/
* **git**: https://git-scm.com/downloads
* **Flutter**: https://docs.flutter.dev/get-started/install/macos
* **Xcode**: Install from the Mac App Store, then open it, agree to license, and install command line tools with `xcode-select --install`.
* **Android Studio** (optional for Android development): https://developer.android.com/studio
* **FVM** - Flutter Version Manager: https://fvm.app/documentation/getting-started/installation
* **CocoaPods**: `sudo gem install cocoapods`
* **Visual Studio Code**: https://code.visualstudio.com/

### Clone the repository

```bash
git clone https://github.com/flet-dev/flet.git
cd flet
```

### Install Flutter

Follow the [official guide](https://docs.flutter.dev/get-started/install/macos) to install Flutter. Ensure Flutter is in your PATH and run `fvm flutter doctor` to verify.

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Set up Python SDK

```bash
cd sdk/python
uv sync
```

### Set up Flutter client

```bash
cd client
fvm flutter pub get
```

### Set environment variables

Add the following to your shell profile (e.g., `~/.zshrc`):

```bash
export FLET_VIEW_PATH="$HOME/flet/client/build/macos/Build/Products/Release"
export FLET_WEB_PATH="$HOME/flet/client/build/web"
```

Then reload: `source ~/.zshrc`

### Build Flutter client

```bash
cd client
fvm flutter build macos
fvm flutter build web --wasm
```

### Verify installation

Create a `hello.py` file with the updated example and run it with `uv run python hello.py`. You should see a window with "Hello, world!".

### Running tests

```bash
cd sdk/python
uv run pytest
```

### Additional notes

* For Android development, set up an Android emulator or connect a physical device.
* For iOS development, you need Xcode and a Mac with Apple Silicon or an Intel Mac.
* Refer to the official Flutter documentation for any platform-specific setup.
