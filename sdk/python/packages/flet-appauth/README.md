# flet-appauth

[![pypi](https://img.shields.io/pypi/v/flet-appauth.svg)](https://pypi.python.org/pypi/flet-appauth)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-appauth)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-appauth/LICENSE)

A [Flet](https://flet.dev) service that wraps
[`flutter_appauth`](https://pub.dev/packages/flutter_appauth) for native
OAuth 2.0 authorization-code + PKCE on Android and iOS.

Used by [`page.login()`](https://docs.flet.dev/cookbook/authentication) on
mobile. Token exchange remains in Python (`AuthorizationService`).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

## Installation

```bash
uv add flet-appauth
# or
pip install flet-appauth
# or
pip install 'flet[appauth]'
```

Configure an AppAuth redirect scheme for `flet build` (see
[documentation](https://docs.flet.dev/appauth)).

## Documentation

https://docs.flet.dev/appauth/
