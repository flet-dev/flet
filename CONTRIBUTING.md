# Contributing to Flet

Thank you for your interest in contributing to Flet!

## Clone repo

```
git clone https://github.com/flet-dev/flet
```

## Python SDK

### Install Poetry

#### Windows

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Be sure to add `%USERPROFILE%\AppData\Roaming\Python\Scripts` to `PATH`.

#### macOS

```
curl -sSL https://install.python-poetry.org | python3 -
```

### Open worker directory

```
cd sdk/python
```

### Install dependencies

To install all Flet dependencies and enable the project as editable package run:

```
poetry install
```

### Check the installation

Create `hello.py` file with a minimal Flet program:

```python
import flet
from flet import Page, Text

def main(page: Page):
    page.add(Text("Hello, world!"))

flet.app(target=main)
```

and then run it:

```
poetry run python hello.py
```

During the first run Flet Client (`flet`) executable will be downloaded from [Flet GitHub releases](https://github.com/flet-dev/flet/releases) to a user temp directory and then started from there. The version of release to download from is taken from `flet/version.py` file.

You should see a new native OS window opened with "Hello, world!" in it.

### Running tests

Pytest should be run with `poetry run`:

```
poetry run pytest
```

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

[pre-commit](https://pre-commit.com) is a dev dependency of Flet and is automatically installed by `poetry install`.
To install the pre-commit hooks run: `poetry run pre-commit install`.
Once installed, every time you commit, pre-commit will run the configured hooks against changed files.

## Possible installation error when working with a source package

When you run python3 hello.py, you might encounter an error like this:
`FileNotFoundError: [Error 2] No such file or directory: '/var/folders/xm/cyv42vbs27gff3s39vy97rx00000gn/T/fletd-0.1.50/fletd'`

To resolve the issue, just delete this folder `../T/fletd-0.1.50/fletd`. The folder is the one with the FileNotFound Error encountered earlier.

It should work now.

## Flutter client

Add the `FLET_VIEW_PATH` and `FLET_WEB_PATH` variables to the environment variables or profile scripts for your respective OS, making sure to modify the path accordingly:

- On macOS (in `~/.zprofile` or any other profile script):
```
# Flet
export FLET_VIEW_PATH="$HOME/{path-to-flet}/flet/client/build/macos/Build/Products/Release"
export FLET_WEB_PATH="$HOME/{path-to-flet}/flet/client/build/web"
```

- On Windows (open "System Properties" > "Environment Variables", then add a new environment variable):
  - as "Variable name", enter `FLET_VIEW_PATH`, and as "Value", `{path-to-flet}\flet\client\build\windows\x64\runner\Release`
  - as "Variable name", enter `FLET_WEB_PATH`, and as "Value", `{path-to-flet}\flet\client\build\web`

- On Linux (in `~/.bash_profile` or any other profile script):
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

### Building the Flutter client
Open an instance of your IDE (preferably VS Code) at the `flet-dev/flet/client` directory.

First, run `printenv | grep FLET` (or `gci env:* | findstr FLET` on Windows) in the built-in terminal to make sure everything is set. You should see the above environment variables you set (`FLET_VIEW_PATH`, `FLET_WEB_PATH`) printed out.

-  To build the Flutter client for MacOS, run:
    ```
    flutter build macos
    ```
    When the build is complete, you should see the Flet bundle in the `FLET_VIEW_PATH`. (Running it will open a blank window.)
-  To build the Flutter client for Web, run the below command:
    ```
    flutter build web
    ```   
    When the build is complete, a directory `client/build/web` will be created.

### Running the Flutter client
Now open another instance of VS Code at `flet-dev/flet/sdk/python` directory.

Create a new folder preferably named `playground` (it has been added to the gitignore) in which you will test your additions.

Try running the below command, where `<your-main.py>` is the file to test your additions:

```bash
poetry run flet run -w -p 8550 playground/<your-main.py>
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
    poetry run flet run -w -p 8550 playground/<your-main.py>
    ```

## Releasing Flet

* Create a new `prepare-{version}` branch in [flet-dev/flet](https://github.com/flet-dev/flet) repository.
* For every package in `packages/flet*` directory:
  * Update package version to `{version}` in `pubspec.yaml`.
  * Add `# {version}` with new/changed/fixed items into `CHANGELOG.md`. Only `packages/flet/CHANGELOG.md` should contain real items; other packages could have just a stub.
* Copy `# {version}` section from `packages/flet/CHANGELOG.md` to the root `CHANGELOG.md`.
* Open terminal in `client` directory and run `flutter pub get` to update Flet dependency versions in `client/pubspec.lock`.
* Create a new `{version}` branch in [flet-dev/flet-app-templates](https://github.com/flet-dev/flet-app-templates) repository from a previously released `{current-version}` branch.
* Create a new `{version}` branch in [flet-dev/flet-build-template](https://github.com/flet-dev/flet-build-template) repository from a previously released `{current-version}` branch.
* Create `Prepare Flet {version}` PR to merge into `main` branch.
* In `Build Flet package for Flutter` job of [Flet CI build](https://ci.appveyor.com/project/flet-dev/flet) make sure analysis report of every `flet*` Flutter package has only 1 issue "Publishable packages can't have 'path' dependencies.".
* Merge `Prepare Flet {version}` PR.
* Create and push new `v{version}` tag (with `v` prefix).
* Update release notes at `https://github.com/flet-dev/flet/releases/tag/v{version}`.

## New macOS environment for Flet developer

* **Homebrew**: https://brew.sh/

After installing homebrew, install xz libraries with it:
```
brew install xz
```

* **Pyenv**. Install with `brew`: https://github.com/pyenv/pyenv?tab=readme-ov-file#unixmacos
  * Install and switch to the latest Python 3.12:
```
pyenv install 3.12.6
pyenv global 3.12.6
```

Setup your shell environment: https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zprofile
```

Ensure Python version is 3.12.6 and location is `/Users/{user}/.pyenv/shims/python`:

```
python --version
which python
```

* **Rbenv**. Install with `brew`: https://github.com/rbenv/rbenv?tab=readme-ov-file#homebrew
  * Install and switch to the latest Ruby:
```
rbenv install 3.3.5
rbenv global 3.3.5
```

Ensure Ruby version is 3.3.5 and location is `/Users/{user}/.rbenv/shims/ruby`:

```
ruby --version
which ruby
```

* **VS Code**. Install "Apple silicon" release: https://code.visualstudio.com/download

* **GitHub Desktop**: https://desktop.github.com/download/
Open GitHub Desktop app, install Rosetta.

* **Poetry**: https://python-poetry.org/docs/#installing-with-the-official-installer

After installing poetry, set PATH:
```
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.zprofile
```

Check Poetry version and make sure it's in PATH:

```
poetry --version
```

* **Android Studio** for Android SDK required by Flutter: https://developer.android.com/studio
* **XCode** for macOS and iOS SDKs: https://apps.apple.com/ca/app/xcode/id497799835?mt=12
* **FVM** - Flutter Version Manager: https://fvm.app/documentation/getting-started/installation
Install flutter with fvm:
```
fvm install 3.24.3
fvm global 3.24.3
```

Set PATH:
```
echo 'export PATH=$HOME/fvm/default/bin:$PATH' >> ~/.zprofile
```

* **cocoapods**: https://guides.cocoapods.org/using/getting-started.html#installation