"""Helpers for wiring AppAuth OAuth redirect scheme into Flutter mobile projects."""

from __future__ import annotations

import plistlib
import re
from pathlib import Path
from typing import Callable, Optional


def resolve_appauth_redirect_scheme(
    *,
    cli_scheme: Optional[str],
    get_pyproject: Callable[..., Optional[str]],
    config_platform: Optional[str] = None,
) -> Optional[str]:
    """
    Resolve AppAuth redirect scheme (lowercase) from CLI or pyproject.

    Precedence:
    1. CLI `--appauth-redirect-scheme`
    2. `tool.flet.<android|ios>.appauth.redirect_scheme` for the build platform
    3. `tool.flet.appauth.redirect_scheme`
    """
    if cli_scheme:
        return str(cli_scheme).strip().lower() or None

    if config_platform:
        value = get_pyproject(
            f"tool.flet.{config_platform}.appauth.redirect_scheme"
        )
        if value:
            return str(value).strip().lower() or None

    value = get_pyproject("tool.flet.appauth.redirect_scheme")
    if value:
        return str(value).strip().lower() or None
    return None


def patch_android_appauth_scheme(flutter_dir: Path, scheme: str) -> bool:
    """
    Ensure Android `appAuthRedirectScheme` manifest placeholder is set.

    Returns:
        True if a file was modified (or already had the correct scheme).
        False if no gradle file was found or the placeholder could not be set.
    """
    scheme = scheme.lower()
    candidates = [
        flutter_dir / "android" / "app" / "build.gradle.kts",
        flutter_dir / "android" / "app" / "build.gradle",
    ]
    replace_patterns = [
        # Groovy: [appAuthRedirectScheme: 'old'] or ["appAuthRedirectScheme": "old"]
        r'(["\']?appAuthRedirectScheme["\']?\s*:\s*)["\'][^"\']*["\']',
        # Kotlin mapOf: "appAuthRedirectScheme" to "old"
        r'(["\']appAuthRedirectScheme["\']\s+to\s+)["\'][^"\']*["\']',
        # Kotlin indexed: manifestPlaceholders["appAuthRedirectScheme"] = "old"
        r'(manifestPlaceholders\[["\']appAuthRedirectScheme["\']\]\s*=\s*)["\'][^"\']*["\']',
        # Assignment form: appAuthRedirectScheme = "old"
        r'(appAuthRedirectScheme\s*=\s*)["\'][^"\']*["\']',
    ]

    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "appAuthRedirectScheme" in text:
            if f'"{scheme}"' in text or f"'{scheme}'" in text:
                # Already configured with this scheme (or coincidental match).
                # Still try to normalize via replace; treat as success if present.
                for pattern in replace_patterns:
                    updated = re.sub(pattern, rf'\1"{scheme}"', text)
                    if updated != text:
                        path.write_text(updated, encoding="utf-8")
                        return True
                # Scheme string already present and no rewrite needed.
                return True

            for pattern in replace_patterns:
                updated = re.sub(pattern, rf'\1"{scheme}"', text)
                if updated != text:
                    path.write_text(updated, encoding="utf-8")
                    return True
            return False

        if path.suffix == ".kts" or path.name.endswith(".kts"):
            needle = "defaultConfig {"
            insert = (
                f"{needle}\n        manifestPlaceholders.putAll("
                f'mapOf("appAuthRedirectScheme" to "{scheme}"))'
            )
            if needle in text:
                path.write_text(text.replace(needle, insert, 1), encoding="utf-8")
                return True
        else:
            needle = "defaultConfig {"
            insert = (
                f"{needle}\n        manifestPlaceholders += "
                f"[appAuthRedirectScheme: '{scheme}']"
            )
            if needle in text:
                path.write_text(text.replace(needle, insert, 1), encoding="utf-8")
                return True
        return False
    return False


def patch_ios_appauth_scheme(flutter_dir: Path, scheme: str) -> bool:
    """
    Ensure iOS `CFBundleURLTypes` includes the AppAuth redirect scheme.

    Returns:
        True if Info.plist was modified or already contained the scheme.
        False if Info.plist was missing.
    """
    scheme = scheme.lower()
    plist_path = flutter_dir / "ios" / "Runner" / "Info.plist"
    if not plist_path.exists():
        return False

    with plist_path.open("rb") as f:
        data = plistlib.load(f)

    url_types = data.get("CFBundleURLTypes")
    if not isinstance(url_types, list):
        url_types = []

    for entry in url_types:
        schemes = entry.get("CFBundleURLSchemes") if isinstance(entry, dict) else None
        if isinstance(schemes, list) and scheme in schemes:
            return True

    url_types.append(
        {
            "CFBundleTypeRole": "Editor",
            "CFBundleURLSchemes": [scheme],
        }
    )
    data["CFBundleURLTypes"] = url_types
    with plist_path.open("wb") as f:
        plistlib.dump(data, f)
    return True
