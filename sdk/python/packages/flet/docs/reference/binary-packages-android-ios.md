Binary Python packages (vs "pure" Python packages written in Python only) are packages that partially written in C, Rust or other languages producing native code. Example packages are `numpy`, `cryptography`, or `pydantic`.

Flet provides an alternative index https://pypi.flet.dev to host Python binary wheels (`.whl` files downloaded by pip) for iOS and Android platforms.

This is the list of packages that are currently available for Android and iOS (generated from https://pypi.flet.dev):

{{ flet_pypi_index() }}

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
