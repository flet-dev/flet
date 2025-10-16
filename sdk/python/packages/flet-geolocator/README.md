# flet-geolocator

[![pypi](https://img.shields.io/pypi/v/flet-geolocator.svg)](https://pypi.python.org/pypi/flet-geolocator)
[![downloads](https://static.pepy.tech/badge/flet-geolocator/month)](https://pepy.tech/project/flet-geolocator)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-geolocator/LICENSE)

Adds geolocation capabilities to your [Flet](https://flet.dev) apps.

Features include:
- Get the last known location;
- Get the current location of the device;
- Get continuous location updates;
- Check if location services are enabled on the device.

It is based on the [geolocator](https://pub.dev/packages/geolocator) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/geolocator/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-geolocator` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-geolocator
    ```

- Using `pip`:
    ```bash
    pip install flet-geolocator
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/examples/controls/geolocator).
