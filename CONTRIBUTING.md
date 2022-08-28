# Contributing to Flet

Thank you for your interest in contributing to Flet!

## Clone repo

```
git clone https://github.com/flet-dev/flet
```

## Python SDK

### Install PDM

#### Windows

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -
```

Enable PEP 582:

```
pdm --pep582
```

Run `refreshenv` after installing PDM on Windows or restart terminal.

#### macOS

```
brew install pdm
```

Enable PEP 582:

```
pdm --pep582 >> ~/.zprofile
```

Restart the terminal session to take effect.

### Open worker directory

```
cd sdk/python
```

### Install dependencies

To install all Flet dependencies and enable the project as editable package run:

```
pdm install
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
python3 hello.py
```

During the first run Flet Server (`fletd`) and Flet Client (`flet`) executables will be downloaded from [Flet GitHub releases](https://github.com/flet-dev/flet/releases) to a user temp directory and then started from there. The version of release to download from is taken from `flet/version.py` file.

You should see a new native OS window opened with "Hello, world!" in it.

### Running tests

Pytest should be run with `pdm run`:

```
pdm run pytest
```

### Code formatting

The project uses [Black](https://github.com/psf/black) formatting style. All `.py` files in a PR must be black-formatted.

IDE-specific Black integration guides:

* [VSCode: Using Black to automatically format Python](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0)

#### Type checking

Enable "pylance" type checking in VS Code.

Open user settings, search by "pylance", scroll down to **Python > Analysis: Type checking mode** section. Enable *basic* mode.

#### Sort imports on Save

VS Code includes "isort" by default.

Add the following to user's `settings.json` :

```json
"[python]": {
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
},
"python.sortImports.args": [
    "--trailing-comma",
    "--use-parentheses",
    "--line-width",
    "88",
    "--multi-line",
    "3",
    "--float-to-top"
],
```

All isort command line options can be found [here](https://pycqa.github.io/isort/docs/configuration/options.html).

### pre-commit

[pre-commit](https://pre-commit.com) is a dev dependency of Flet and is automatically installed by `pdm install`.
To install the pre-commit hooks run: `pre-commit install`.
Once installed, everytime you commit, pre-commit will run the configured hooks against changed files.

## Flutter client

TBD
