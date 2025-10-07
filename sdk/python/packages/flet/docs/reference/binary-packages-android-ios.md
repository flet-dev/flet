Binary Python packages (vs "pure" Python packages written in Python only) are packages that partially written in C, Rust or other languages producing native code. Example packages are `numpy`, `cryptography`, or `pydantic`.

Flet provides an alternative index https://pypi.flet.dev to host Python binary wheels (`.whl` files downloaded by pip) for iOS and Android platforms.

This is the list of packages that are currently available for Android and iOS:

| Name                   | Version   |
|------------------------|-----------|
| aiohttp                | 3.9.5     |
| argon2-cffi-bindings   | 21.2.0    |
| bcrypt                 | 4.2.0     |
| bitarray               | 2.9.2     |
| blis                   | 1.0.0     |
| Brotli                 | 1.1.0     |
| cffi                   | 1.17.1    |
| contourpy              | 1.3.0     |
| cryptography           | 43.0.1    |
| fiona                  | 1.10.1    |
| GDAL                   | 3.10.0    |
| google-crc32           | 1.6.0     |
| grpcio                 | 1.67.1    |
| jq                     | 1.8.0     |
| kiwisolver             | 1.4.7     |
| lru-dict               | 1.3.0     |
| lxml                   | 5.3.0     |
| MarkupSafe             | 2.1.5     |
| matplotlib             | 3.9.2     |
| msgpack                | 1.1.0     |
| msgspec                | 0.8.16    |
| numpy                  | 2.1.1     |
| numpy                  | 1.26.4    |
| opaque                 | 0.2.0     |
| opencv-python          | 4.10.0.84 |
| pandas                 | 2.2.2     |
| pendulum               | 3.0.0     |
| pillow                 | 10.4.0    |
| protobuf               | 5.28.3    |
| pycryptodome           | 3.21.0    |
| pycryptodomex          | 3.21.0    |
| pydantic-core          | 2.23.3    |
| pyjnius (Android only) | 1.6.1     |
| PyNaCl                 | 1.5.0     |
| pyobjus (iOS only)     | 1.2.3     |
| pyogrio                | 0.10.0    |
| pyproj                 | 3.7.0     |
| pysodium               | 0.7.18    |
| PyYAML                 | 6.0.2     |
| regex                  | 2024.11.6 |
| ruamel.yaml.clib       | 0.2.12    |
| shapely                | 2.0.6     |
| SQLAlchemy             | 2.0.36    |
| time-machine           | 2.16.0    |
| websockets             | 13.0.1    |
| yarl                   | 1.11.1    |
| zstandard              | 0.23.0    |

/// admonition | Work in progress
    type: danger
New packages can be built with creating a recipe in [Mobile Forge](https://github.com/flet-dev/mobile-forge) project.
For now, Flet team is authoring those recipes for you, but when the process is polished and
fully-automated you'll be able to send a PR and test the compiled package right away.

If you don't yet see a package at https://pypi.flet.dev you can request it in
[Flet discussions - Packages](https://github.com/flet-dev/flet/discussions/categories/packages). Please do not request pure Python packages.
Go to package's "Download files" section at https://pypi.org and make sure it contains
binary platform-specific wheels.
///
