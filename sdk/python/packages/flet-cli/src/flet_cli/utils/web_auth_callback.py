"""Helpers for wiring WebAuth callback scheme into Flutter mobile projects."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, NamedTuple, Optional

# RFC 3986 scheme: ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
_SCHEME_SAFE = re.compile(r"[^a-z0-9+.-]+")


class ResolvedWebAuthScheme(NamedTuple):
    scheme: Optional[str]
    source: str


def sanitize_callback_scheme(name: str) -> Optional[str]:
    """Turn a product/project/bundle id into a valid URL scheme fragment."""
    raw = str(name).strip().lower().replace("_", "-").replace(" ", "-")
    cleaned = _SCHEME_SAFE.sub("", raw).strip(".-+")
    if not cleaned or not cleaned[0].isalpha():
        return None
    return cleaned


def default_callback_scheme_from_bundle_id(
    get_pyproject: Callable[..., Optional[str]],
    *,
    config_platform: Optional[str] = None,
) -> ResolvedWebAuthScheme:
    """
    Default scheme: ``<bundle id>.auth``.

    Bundle id sources (first hit wins):
    ``tool.flet.<platform>.bundle_id``, ``tool.flet.bundle_id``,
    ``tool.flet.org`` + project/artifact name, then sanitized project name + ``.auth``.
    """
    keys = []
    if config_platform:
        keys.append(f"tool.flet.{config_platform}.bundle_id")
    keys.extend(
        [
            "tool.flet.bundle_id",
            "tool.flet.android.bundle_id",
            "tool.flet.ios.bundle_id",
        ]
    )
    for key in keys:
        value = get_pyproject(key)
        if value:
            scheme = str(value).strip().lower() + ".auth"
            if scheme[0].isalpha():
                return ResolvedWebAuthScheme(scheme, f"bundle id ({key})")

    org = get_pyproject("tool.flet.org")
    name = (
        get_pyproject("tool.flet.product")
        or get_pyproject("tool.flet.project")
        or get_pyproject("tool.flet.artifact")
        or get_pyproject("project.name")
    )
    if org and name:
        scheme = (
            f"{str(org).strip().lower()}."
            f"{sanitize_callback_scheme(str(name))}.auth"
        )
        return ResolvedWebAuthScheme(scheme, "tool.flet.org + app name")

    if name:
        base = sanitize_callback_scheme(str(name))
        if base:
            return ResolvedWebAuthScheme(f"{base}.auth", f"app name ({name!r})")

    return ResolvedWebAuthScheme("flet.auth", "fallback (flet.auth)")


def resolve_web_auth_callback_scheme_info(
    *,
    cli_scheme: Optional[str],
    get_pyproject: Callable[..., Optional[str]],
    config_platform: Optional[str] = None,
) -> ResolvedWebAuthScheme:
    """
    Resolve WebAuth callback scheme.

    Precedence:
    1. CLI ``--web-auth-callback-scheme``
    2. ``tool.flet.<platform>.web_auth.callback_scheme``
    3. ``tool.flet.web_auth.callback_scheme``
    4. Default ``<bundle id>.auth``
    """
    if cli_scheme:
        scheme = str(cli_scheme).strip().lower() or None
        return ResolvedWebAuthScheme(
            scheme, "CLI --web-auth-callback-scheme" if scheme else "CLI (empty)"
        )

    if config_platform:
        key = f"tool.flet.{config_platform}.web_auth.callback_scheme"
        value = get_pyproject(key)
        if value:
            return ResolvedWebAuthScheme(str(value).strip().lower() or None, key)

    key = "tool.flet.web_auth.callback_scheme"
    value = get_pyproject(key)
    if value:
        return ResolvedWebAuthScheme(str(value).strip().lower() or None, key)

    return default_callback_scheme_from_bundle_id(
        get_pyproject, config_platform=config_platform
    )


def resolve_web_auth_callback_scheme(
    *,
    cli_scheme: Optional[str],
    get_pyproject: Callable[..., Optional[str]],
    config_platform: Optional[str] = None,
) -> Optional[str]:
    return resolve_web_auth_callback_scheme_info(
        cli_scheme=cli_scheme,
        get_pyproject=get_pyproject,
        config_platform=config_platform,
    ).scheme


def patch_android_web_auth_scheme(flutter_dir: Path, scheme: str) -> bool:
    """Ensure Android manifest placeholder ``webAuthCallbackScheme`` is set."""
    scheme = scheme.lower()
    candidates = [
        flutter_dir / "android" / "app" / "build.gradle.kts",
        flutter_dir / "android" / "app" / "build.gradle",
    ]
    name = "webAuthCallbackScheme"
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        patterns = [
            rf'(["\']?{name}["\']?\s*:\s*)["\'][^"\']*["\']',
            rf'(["\']{name}["\']\s+to\s+)["\'][^"\']*["\']',
            rf'(manifestPlaceholders\[["\']{name}["\']\]\s*=\s*)["\'][^"\']*["\']',
            rf'({name}\s*=\s*)["\'][^"\']*["\']',
        ]
        updated = text
        for pattern in patterns:
            updated = re.sub(pattern, rf'\1"{scheme}"', updated)

        if updated != text:
            path.write_text(updated, encoding="utf-8")
            return True

        needle = "defaultConfig {"
        if needle not in text:
            return False
        if path.suffix == ".kts" or path.name.endswith(".kts"):
            insert = (
                f"{needle}\n        manifestPlaceholders.putAll("
                f'mapOf("{name}" to "{scheme}"))'
            )
        else:
            insert = (
                f"{needle}\n        manifestPlaceholders += "
                f"[{name}: '{scheme}']"
            )
        path.write_text(text.replace(needle, insert, 1), encoding="utf-8")
        return True
    return False
