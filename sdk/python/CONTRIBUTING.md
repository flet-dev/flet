# Contributing to Flet for Python

Thank you for your interest in contributing to Flet!

## Clone repo

```
git clone https://github.com/flet-dev/flet
```

## Install PDM

### Windows

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -
```

Enable PEP 582:

```
pdm --pep582
```

Run `refreshenv` after installing PDM on Windows or restart terminal.

### macOS

```
brew install pdm
```

Enable PEP 582:

```
pdm --pep582 >> ~/.zprofile
```

Restart the terminal session to take effect.

## Open worker directory

```
cd flet/sdk/python
```

## Install dependencies

To install all Flet dependencies and enable the project as editable package run:

```
pdm install
```

## Check the installation

Run "counter" example:

```
python3 examples/counter.py
```

During the first run Flet Server will be downloaded from GitHub releases to `$HOME/.flet/bin` directory and started from there. The version of Flet Server to download is taken from `FLET_VERSION` variable in `appveyor.yml` in the root of repository.

You should see a new browser window opened with "counter" web app running.

## Running tests

Pytest should be run with `pdm run`:

```
pdm run pytest
```

## Code formatting

The project uses [Black](https://github.com/psf/black) formatting style. All `.py` files in a PR must be black-formatted.

IDE-specific Black integration guides:

* [VSCode: Using Black to automatically format Python](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0)

### Sort imports on Save

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

## pre-commit

[pre-commit](https://pre-commit.com) is a dev dependency of Flet and is automatically installed by `pdm install`.
To install the pre-commit hooks run: `pre-commit install`.
Once installed, everytime you commit, pre-commit will run the configured hooks against changed files.
