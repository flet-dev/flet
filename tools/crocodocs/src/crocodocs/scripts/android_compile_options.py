"""Render Android compiler documentation from the CLI defaults."""

import json


def android_compile_options_defaults() -> str:
    """Render the default compile options as a TOML code block."""
    from flet_cli.commands.build_base import DEFAULT_ANDROID_COMPILE_OPTIONS

    toml = "\n".join(
        f"{name} = {json.dumps(expression)}"
        for name, expression in DEFAULT_ANDROID_COMPILE_OPTIONS.items()
    )
    return f"""```toml
[tool.flet.android.compile_options]
{toml}
```
"""


def android_compile_options_example() -> str:
    """Render the compile-options example's Gradle translation using CLI defaults."""
    from flet_cli.commands.build_base import DEFAULT_ANDROID_COMPILE_OPTIONS

    options = {
        **DEFAULT_ANDROID_COMPILE_OPTIONS,
        "sourceCompatibility": "JavaVersion.VERSION_1_8",
        "encoding": '"ISO-8859-1"',
    }
    kotlin = "\n".join(
        f"    {name} = {expression}" for name, expression in options.items()
    )
    return f"""```kotlin
compileOptions {{
{kotlin}
}}
```
"""


if __name__ == "__main__":
    print(android_compile_options_defaults())
