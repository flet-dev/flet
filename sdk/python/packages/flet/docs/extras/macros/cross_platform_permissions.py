import argparse


def _indent_block(text: str, indent: int) -> str:
    prefix = " " * indent
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


def _toml_key(key: str) -> str:
    if key.replace("-", "").replace("_", "").isalnum():
        return key
    escaped = key.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _toml_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _load_cross_platform_permissions() -> dict:
    from flet_cli.commands.build_base import BaseBuildCommand

    parser = argparse.ArgumentParser(add_help=False)
    command = BaseBuildCommand(parser)
    return command.cross_platform_permissions


def _render_toml_block(config: dict) -> str:
    info_plist = config.get("info_plist") or {}
    macos_entitlements = config.get("macos_entitlements") or {}
    android_permissions = config.get("android_permissions") or {}
    android_features = config.get("android_features") or {}

    sections = []

    if info_plist:
        lines = ["# iOS", "[tool.flet.ios.info]"]
        for key, value in info_plist.items():
            lines.append(f"{_toml_key(key)} = {_toml_value(value)}")
        sections.append("\n".join(lines))

        lines = ["# macOS", "[tool.flet.macos.info]"]
        for key, value in info_plist.items():
            lines.append(f"{_toml_key(key)} = {_toml_value(value)}")
        if macos_entitlements:
            lines.extend(["", "[tool.flet.macos.entitlement]"])
            for key, value in macos_entitlements.items():
                lines.append(f"{_toml_key(key)} = {_toml_value(value)}")
        sections.append("\n".join(lines))

    if android_permissions:
        lines = ["# Android", "[tool.flet.android.permission]"]
        for key, value in android_permissions.items():
            lines.append(f"{_toml_key(key)} = {_toml_value(value)}")
        if android_features:
            lines.extend(["", "[tool.flet.android.feature]"])
            for key, value in android_features.items():
                lines.append(f"{_toml_key(key)} = {_toml_value(value)}")
        sections.append("\n".join(lines))

    return "\n\n".join(sections)


def cross_platform_permissions_list() -> str:
    permissions = _load_cross_platform_permissions()
    items = []
    for name, config in permissions.items():
        toml_block = _indent_block(_render_toml_block(config), 4)
        items.append(
            "\n".join(
                [
                    f"- `{name}`",
                    "",
                    "    /// details | `pyproject.toml` equivalent",
                    "        type: example",
                    "    ```toml",
                    toml_block,
                    "    ```",
                    "    ///",
                ]
            )
        )

    return "\n\n".join(items) + "\n"


if __name__ == "__main__":
    print(cross_platform_permissions_list())
