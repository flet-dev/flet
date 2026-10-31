# flet-quick-actions

[![pypi](https://img.shields.io/pypi/v/flet-quick-actions.svg)](https://pypi.python.org/pypi/flet-quick-actions)
[![downloads](https://static.pepy.tech/badge/flet-quick-actions/month)](https://pepy.tech/project/flet-quick-actions)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-quick-actions)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-quick-actions.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-quick-actions.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-quick-actions/LICENSE)

Adds home-screen quick actions to your [Flet](https://flet.dev) apps.


Features include:
- Set dynamic shortcuts shown when the user long-presses the app icon;
- Clear all installed quick actions;
- Listen for quick-action taps, including the cold-start action that launched the app.

It is based on the [quick_actions](https://pub.dev/packages/quick_actions) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/services/quickactions/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

Quick actions are a mobile-only OS feature.

## Usage

### Installation

To install the `flet-quick-actions` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-quick-actions
    ```
- Using pip:
    ```bash
    pip install flet-quick-actions
    ```

After this, you will have to manually add this package to your requirements.txt or pyproject.toml.