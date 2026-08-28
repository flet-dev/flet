"""Assert on a `flet build linux` bundle's icon and desktop integration.

TEMPORARY -- part of the issue #2269 Linux icon verification harness.

Everything here is checkable without a display. The build having succeeded at
all is itself the headline check: it is the only proof that the Linux runner's
C changes compile, which cannot be verified on macOS.

Usage: assert_bundle.py <leg> <app_dir> <repo_root>
"""

import hashlib
import html.parser
import json
import sys
from pathlib import Path

import yaml

BUNDLE_ID = "com.flet.flet-icon-test"
PRODUCT = "Flet Icon Test"

# leg -> (artifact name, icon source relative to the app, theme dir)
LEGS = {
    "default": ("flet-icon-test", None, "256x256"),
    "themed": ("flet-icon-test", "src/assets/icon_linux.png", "256x256"),
    "large": ("flet-icon-test", "src/assets/icon_linux.png", "512x512"),
    "hostile": ("flet icon test", "src/assets/icon_linux.png", "256x256"),
}

failures: list[str] = []
checks = 0


def check(ok: bool, label: str, detail: str = "") -> bool:
    global checks
    checks += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"    {detail}" if detail else ""))
    if not ok:
        failures.append(label)
    return ok


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path):
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def parse_desktop_entry(text: str) -> dict:
    entry = {}
    in_section = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            in_section = line == "[Desktop Entry]"
            continue
        if in_section and "=" in line and not line.startswith("#"):
            key, _, value = line.partition("=")
            entry[key] = value
    return entry


class MetaDescription(html.parser.HTMLParser):
    """Pull the meta description out, so newlines in it can't fool a grep."""

    def __init__(self):
        super().__init__()
        self.content = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and d.get("name") == "description":
            self.content = d.get("content")


def main() -> int:
    leg, app_dir, repo_root = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    artifact, icon_rel, theme_dir = LEGS[leg]
    bundle = app_dir / "build" / "linux"
    flutter_dir = app_dir / "build" / "flutter"

    print(f"== leg: {leg} (artifact={artifact!r}, theme dir={theme_dir})")

    # --- the runner compiled and is runnable -------------------------------
    exe = bundle / artifact
    if check(exe.is_file(), f"runner binary exists: build/linux/{artifact}"):
        check(exe.stat().st_mode & 0o111 != 0, "runner binary is executable")

    # --- window icon --------------------------------------------------------
    icon = bundle / "data" / "app_icon.png"
    if check(icon.is_file(), "bundle ships data/app_icon.png"):
        size = png_size(icon)
        check(size is not None, "data/app_icon.png is a real PNG", f"size={size}")
        source = (
            app_dir / icon_rel
            if icon_rel
            else repo_root
            / "sdk/python/templates/build/{{cookiecutter.out_dir}}/images/icon.png"
        )
        check(
            sha256(icon) == sha256(source),
            "data/app_icon.png is byte-identical to the source icon",
            f"source={source.name}",
        )

    # --- freedesktop tree ---------------------------------------------------
    themed_icon = (
        bundle / "share" / "icons" / "hicolor" / theme_dir / "apps" / f"{BUNDLE_ID}.png"
    )
    check(
        themed_icon.is_file(),
        f"themed icon installed into hicolor/{theme_dir}",
    )
    if themed_icon.is_file():
        size = png_size(themed_icon)
        expected = int(theme_dir.split("x")[0])
        check(
            size == (expected, expected) or theme_dir == "256x256",
            "themed icon size matches its icon-theme directory",
            f"size={size} dir={theme_dir}",
        )

    desktop = bundle / "share" / "applications" / f"{BUNDLE_ID}.desktop"
    if check(desktop.is_file(), f"desktop entry installed: {desktop.name}"):
        text = desktop.read_text(encoding="utf-8")
        entry = parse_desktop_entry(text)
        check(entry.get("Type") == "Application", "Type=Application")
        check(entry.get("Name") == PRODUCT, "Name comes from --product", entry.get("Name", ""))
        # Quoted so an artifact name with spaces stays one argument.
        check(
            entry.get("Exec") == f'"{artifact}" %U',
            "Exec is quoted and names the artifact",
            entry.get("Exec", ""),
        )
        check(entry.get("Icon") == BUNDLE_ID, "Icon is the themed bundle id")
        check(
            entry.get("StartupWMClass") == BUNDLE_ID,
            "StartupWMClass matches the app id set by g_set_prgname",
        )
        check(
            entry.get("Categories") == "Development;Utility;",
            "Categories come from tool.flet.linux.categories",
            entry.get("Categories", ""),
        )
        comment = entry.get("Comment", "")
        check(
            "\n" not in comment and "\t" not in comment,
            "Comment carries no raw control characters",
            repr(comment),
        )
        if leg == "hostile":
            check("\\\\path" in comment, "backslash in Comment is escaped", repr(comment))

    # --- the description reached every generated file, still parseable ------
    description = (app_dir / "pyproject.toml").read_text(encoding="utf-8")
    expected_description = None
    for line in description.splitlines():
        if line.startswith("description = "):
            expected_description = json.loads(line.split(" = ", 1)[1])
            break

    pubspec = flutter_dir / "pubspec.yaml"
    if check(pubspec.is_file(), "generated pubspec.yaml exists"):
        try:
            parsed = yaml.safe_load(pubspec.read_text(encoding="utf-8"))
            check(
                parsed.get("description") == expected_description,
                "pubspec.yaml parses and its description round-trips",
                repr(parsed.get("description")),
            )
        except yaml.YAMLError as e:
            check(False, "pubspec.yaml parses", f"<unparsable: {e}>")

    manifest = flutter_dir / "web" / "manifest.json"
    if manifest.is_file():
        try:
            parsed = json.loads(manifest.read_text(encoding="utf-8"))
            check(
                parsed.get("description") == expected_description,
                "manifest.json is valid JSON and its description round-trips",
            )
        except json.JSONDecodeError as e:
            check(False, "manifest.json is valid JSON", f"<unparsable: {e}>")

    index = flutter_dir / "web" / "index.html"
    if index.is_file():
        parser = MetaDescription()
        parser.feed(index.read_text(encoding="utf-8"))
        check(
            parser.content == expected_description,
            "index.html meta description is escaped and round-trips",
        )

    print(f"\n{checks - len(failures)}/{checks} checks passed")
    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
