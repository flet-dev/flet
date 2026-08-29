"""Assert on the `.deb` and AppImage the docs' recipes produced.

Demo branch only.

A reviewer downloads these two files and nothing else, so a mistake here is a
mistake they hit first. Both are checked from the outside, the way a package
manager sees them, rather than from the staging trees the recipes left behind.

Usage: assert_packages.py <deb path> <appimage path>
"""

import io
import subprocess
import sys
import tarfile
from pathlib import Path

BUNDLE_ID = "com.flet.flet_icon_demo"
PKG = "flet-icon-demo"
BIN = "flet-icon-demo"

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


def check_deb(deb: Path) -> None:
    """Check the package's payload the way `dpkg -c` and `apt` would see it."""
    print(f"== {deb.name}")
    if not check(deb.is_file(), "the .deb exists"):
        return

    fsys = subprocess.run(
        ["dpkg-deb", "--fsys-tarfile", str(deb)], capture_output=True, check=True
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(fsys)) as tar:
        members = {m.name.lstrip("."): m for m in tar.getmembers()}

        exe = f"/opt/{PKG}/{BIN}"
        if check(exe in members, f"ships the executable at {exe}"):
            check(members[exe].mode & 0o111 != 0, "the executable keeps its exec bit")

        # /usr/bin must be a symlink: the app finds its bundled Python from the
        # path of the running executable, so a wrapper script would send it
        # looking in /usr/bin.
        link = f"/usr/bin/{PKG}"
        if check(link in members, f"puts {link} on PATH"):
            check(members[link].issym(), f"{link} is a symlink, not a wrapper",
                  members[link].linkname)

        # Nothing under /opt is scanned by the desktop, so these two have to
        # have moved to /usr/share.
        entry_path = f"/usr/share/applications/{BUNDLE_ID}.desktop"
        icon_path = f"/usr/share/icons/hicolor/256x256/apps/{BUNDLE_ID}.png"
        check(icon_path in members, "installs the icon into the system hicolor tree")
        check(
            f"/opt/{PKG}/share" not in members,
            "the bundle's own share/ is not shipped a second time",
        )

        if check(entry_path in members, "installs the desktop entry"):
            entry = tar.extractfile(members[entry_path]).read().decode("utf-8")
            exec_line = next(
                (l for l in entry.splitlines() if l.startswith("Exec=")), ""
            )
            check(
                exec_line == f"Exec=/opt/{PKG}/{BIN} %U",
                "Exec= was rewritten to the install path",
                exec_line,
            )


def check_appimage(appimage: Path) -> None:
    """Check the AppDir layout `appimagetool` packed, by extracting it."""
    print(f"\n== {appimage.name}")
    if not check(appimage.is_file(), "the AppImage exists"):
        return
    check(appimage.stat().st_mode & 0o111 != 0, "the AppImage is executable")

    out = appimage.parent / "squashfs-root"
    subprocess.run(
        [str(appimage), "--appimage-extract"],
        cwd=appimage.parent,
        check=True,
        capture_output=True,
    )
    check((out / "AppRun").is_file(), "AppRun is the entry point")
    check((out / f"{BUNDLE_ID}.desktop").is_file(),
          "a desktop entry sits at the AppDir root")
    check((out / ".DirIcon").exists(),
          ".DirIcon gives the AppImage file its own icon")
    check((out / "usr/bin" / BIN).is_file(),
          "the whole bundle travelled into usr/bin")
    # The app resolves its interpreter relative to its own path, so the
    # python3.x/ directory has to have stayed a sibling of the executable.
    check(any((out / "usr/bin").glob("python3*")),
          "the bundled Python runtime stayed next to it")


def main() -> int:
    check_deb(Path(sys.argv[1]))
    check_appimage(Path(sys.argv[2]))
    print(f"\n{checks - len(failures)}/{checks} checks passed")
    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
