"""Assert on the demo app's `flet build linux` bundle.

Demo branch only.

Everything here is checkable without a display, and runs before the packaging
recipes do -- a bundle that is already wrong would otherwise produce a `.deb`
and an AppImage that install cleanly and show the stock Flutter icon.

Usage: assert_bundle.py <app_dir>
"""

import hashlib
import sys
from pathlib import Path

BUNDLE_ID = "com.flet.flet_icon_demo"
PRODUCT = "Flet Icon Demo"
ARTIFACT = "flet-icon-demo"
ICON_SOURCE = "src/assets/icon_linux.png"
THEME_DIR = "256x256"
CATEGORIES = "Graphics;Viewer;"

failures: list[str] = []
checks = 0


def check(ok: bool, label: str, detail: str = "") -> bool:
    """Record one assertion and print it as a PASS/FAIL line."""
    global checks
    checks += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"    {detail}" if detail else ""))
    if not ok:
        failures.append(label)
    return ok


def png_size(path: Path):
    """The PNG's (width, height), or None if it is not a PNG at all."""
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def parse_desktop_entry(text: str) -> dict:
    """The `[Desktop Entry]` group as a dict, ignoring comments."""
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


def main() -> int:
    app_dir = Path(sys.argv[1])
    bundle = app_dir / "build" / "linux"

    # The build having succeeded at all is the headline check: it is the only
    # proof that the runner's C changes compile, which cannot be checked on
    # macOS or Windows.
    exe = bundle / ARTIFACT
    if check(exe.is_file(), f"runner binary exists: build/linux/{ARTIFACT}"):
        check(exe.stat().st_mode & 0o111 != 0, "runner binary is executable")

    # The window icon, loaded by main() in linux/my_application.cc.
    icon = bundle / "data" / "app_icon.png"
    if check(icon.is_file(), "bundle ships data/app_icon.png"):
        check(png_size(icon) is not None, "data/app_icon.png is a real PNG",
              f"size={png_size(icon)}")
        check(
            hashlib.sha256(icon.read_bytes()).hexdigest()
            == hashlib.sha256((app_dir / ICON_SOURCE).read_bytes()).hexdigest(),
            "data/app_icon.png is byte-identical to the app's icon_linux.png",
        )

    # The launcher icon, which is what the dock and app grid resolve.
    themed = bundle / "share/icons/hicolor" / THEME_DIR / "apps" / f"{BUNDLE_ID}.png"
    if check(themed.is_file(), f"themed icon installed into hicolor/{THEME_DIR}"):
        expected = int(THEME_DIR.split("x")[0])
        check(
            png_size(themed) == (expected, expected),
            "themed icon size matches its icon-theme directory",
            f"size={png_size(themed)}",
        )

    desktop = bundle / "share/applications" / f"{BUNDLE_ID}.desktop"
    if check(desktop.is_file(), f"desktop entry installed: {desktop.name}"):
        entry = parse_desktop_entry(desktop.read_text(encoding="utf-8"))
        check(entry.get("Type") == "Application", "Type=Application")
        check(entry.get("Name") == PRODUCT, "Name is the product name",
              entry.get("Name", ""))
        # Quoted, so an artifact name containing spaces stays one argument.
        check(entry.get("Exec") == f'"{ARTIFACT}" %U',
              "Exec is quoted and names the artifact", entry.get("Exec", ""))
        check(entry.get("Icon") == BUNDLE_ID, "Icon is the themed bundle id")
        check(entry.get("StartupWMClass") == BUNDLE_ID,
              "StartupWMClass matches the app id set by g_set_prgname")
        check(entry.get("Categories") == CATEGORIES,
              "Categories come from tool.flet.linux.categories",
              entry.get("Categories", ""))

    print(f"\n{checks - len(failures)}/{checks} checks passed")
    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
