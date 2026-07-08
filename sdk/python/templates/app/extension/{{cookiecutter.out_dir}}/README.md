# {{cookiecutter.project_name}}

{{cookiecutter.project_name}} [Flet](https://flet.dev) extension.
{% if cookiecutter.description %}
{{ cookiecutter.description }}
{% endif %}
<!--- If your extension wraps a Flutter package, credit it here, ex:
It is based on the [xyz](https://pub.dev/packages/xyz) Flutter package. -->

## Platform Support

<!--- Update the table accordingly for your extension, using ✅ and ❌. -->

| Platform  | iOS | Android | Web | Windows | macOS | Linux |
|-----------|-----|---------|-----|---------|-------|-------|
| Supported | ✅   | ✅       | ✅   | ✅       | ✅     | ✅     |

## Usage

### Installation

Add `{{cookiecutter.project_name}}` dependency to the `pyproject.toml` of your Flet project:

* **From Git**

```toml
dependencies = [
  "{{cookiecutter.project_name}} @ git+https://github.com/MY_GITHUB_ACCOUNT/{{cookiecutter.project_name}}",
  "flet>={{cookiecutter.flet_version}}",
]
```

<!--- Remove below list item, if your extension isn't yet available on PyPI. -->

* **From PyPI**

```toml
dependencies = [
  "{{cookiecutter.project_name}}",
  "flet>={{cookiecutter.flet_version}}",
]
```

### Run your app

A Flet extension has two sides: its Python controls/services and the native Flutter/Dart widgets behind them.
That native code must be compiled into a Flet client before your controls can render, and the
prebuilt client that a plain `flet run` uses does **not** include this extension.

So run your app in one of these two ways:

**1. [`flet debug`](https://flet.dev/docs/cli/flet-debug)** — all platforms: *Windows, macOS, Linux, Web, iOS, Android*

Compiles the extension and launches your app on the target you pick. 
The simplest option, and the way to go for mobile and web:

```bash
flet debug macos                   # desktop & web: no device needed
flet debug android -d <device-id>  # mobile: connect a device/emulator first
```

For iOS and Android, pass `-d <device-id>` (run `flet debug --show-devices` to list connected devices).
Edits to your **Python** code are picked up the next time you run `flet debug`.

**2. [`flet build`](https://flet.dev/docs/cli/flet-build) once, then [`flet run`](https://flet.dev/docs/cli/flet-run)** — desktop only: *Windows, macOS, Linux*

Build a custom client that bundles the extension **once**, then use `flet run` for a fast hot-reload loop while you edit Python:

```bash
flet build macos  # or: flet build windows / flet build linux
flet run          # run from the folder where build/ was created, so it reuses that client
```

`flet run` auto-detects the client under `build/<platform>/`, so your Python edits hot-reload instantly.
Rebuild only when the extension's **Dart** code changes.

### Examples

See the [examples](examples) directory.

### Documentation

<!--- Update the link, if your docs are elsewhere. Alternatively, you could write out all docs in this section directly. -->

Detailed documentation for this package can be found [here](https://MY_GITHUB_ACCOUNT.github.io/{{cookiecutter.project_name}}/).
