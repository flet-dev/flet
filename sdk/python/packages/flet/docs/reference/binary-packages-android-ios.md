Binary Python packages (as opposed to "pure" Python packages written entirely in Python)
contain components written in C, Rust, or other languages that produce native code.
Common examples include `numpy`, `cryptography`, and `pydantic`.

Flet provides an alternative package index, [pypi.flet.dev](https://pypi.flet.dev),
which hosts prebuilt Python binary wheels (`.whl` files used by `pip`) for iOS and Android platforms.

/// admonition | Work in progress
    type: danger
New packages are created by adding a recipe to the
[Mobile Forge](https://github.com/flet-dev/mobile-forge) project.
Currently, we author these recipes for you; once the build process
is fully automated, you'll be able to submit a PR and test the
compiled package immediately.

If a package is not available on [pypi.flet.dev](https://pypi.flet.dev),
you can request it in [Flet discussions - Packages](https://github.com/flet-dev/flet/discussions/categories/packages).
Please do not request "pure" Python packages. Check out this
[guide](https://flet.dev/blog/flet-packaging-update#pure-python-packages)
for more details on the difference between pure and binary packages.
///

Below is the list of packages hosted on [pypi.flet.dev](https://pypi.flet.dev)
and the specific wheel versions currently built and supported:

{{ flet_pypi_index() }}
