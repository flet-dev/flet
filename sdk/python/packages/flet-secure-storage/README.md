# flet-secure-storage

[![pypi](https://img.shields.io/pypi/v/flet-secure-storage.svg)](https://pypi.python.org/pypi/flet-secure-storage)
[![downloads](https://static.pepy.tech/badge/flet-secure-storage/month)](https://pepy.tech/project/flet-secure-storage)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-secure-storage/LICENSE)

A service for safely storing sensitive key–value data using the platform’s native secure storage mechanisms—Keychain on iOS/macOS, Windows Credential Manager, libsecret on Linux, and Keystore on Android.

Powered by Flutter's [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) package.

You need `libsecret-1-dev` on your machine to build the project, and `libsecret-1-0` to run the application (add it as a dependency after packaging your app). If you using snapcraft to build the project use the following.

Apart from `libsecret` you also need a keyring service, for that you need either [`gnome-keyring`](https://wiki.gnome.org/Projects/GnomeKeyring) (for Gnome users) or [`kwalletmanager`](https://wiki.archlinux.org/title/KDE_Wallet) (for KDE users) or other light provider like [`secret-service`](https://github.com/yousefvand/secret-service).

```bash
sudo apt-get install libsecret-1-dev libsecret-1-0
```

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/secure_storage/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-secure-storage` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-secure-storage
    ```

- Using `pip`:
    ```bash
    pip install flet-secure-storage
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/services/secure_storage).
