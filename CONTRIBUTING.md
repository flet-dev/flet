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

IDE-specific Black integration guides:

- [VSCode: Using Black to automatically format Python](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0)

#### Type checking

Enable "pylance" type checking in VS Code.

Open user settings, search by "pylance", scroll down to **Python > Analysis: Type checking mode** section. Enable _basic_ mode.

#### Sort imports on Save

Install `isort` extension for imports formatting: https://marketplace.visualstudio.com/items?itemName=ms-python.isort

### pre-commit

[pre-commit](https://pre-commit.com) is a dev dependency of Flet and is automatically installed by `poetry install`.
To install the pre-commit hooks run: `pre-commit install`.
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
  - as "Variable name", enter `FLET_VIEW_PATH`, and as "Value", `%USERPROFILE%\{path-to-flet}\flet\client\build\windows\x64\runner\Release`
  - as "Variable name", enter `FLET_WEB_PATH`, and as "Value", `%USERPROFILE%\{path-to-flet}\flet\client\build\web`

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

First, run `printenv | grep FLET` in the built-in terminal to make sure everything is set. You should see the above environment variables you set (`FLET_VIEW_PATH`, `FLET_WEB_PATH`) printed out.

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

**Note** that if you make changes to the dart files, you will need to recompile/rebuild the Flutter client (with `flutter run` as above) for the changes to take effect in your playground.
