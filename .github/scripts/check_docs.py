#!/usr/bin/env python3
"""Check built Docusaurus docs for broken images, unresolved xrefs, and missing examples."""

import glob
import os
import re
import sys


def check_broken_images(build_dir: str) -> list[str]:
    img_re = re.compile(r'<img[^>]+src="(/[^"]+)"', re.IGNORECASE)
    errors = []
    for html_file in sorted(
        glob.glob(f"{build_dir}/docs/**/index.html", recursive=True)
    ):
        page = (
            html_file.replace(build_dir + "/", "").replace("/index.html", "")
        )
        content = open(html_file).read()
        for match in img_re.finditer(content):
            src = match.group(1)
            if src.startswith("http") or src.startswith("data:"):
                continue
            file_path = os.path.join(build_dir, src.lstrip("/"))
            if not os.path.exists(file_path):
                errors.append(f"  {page}: {src}")
    return errors


def check_pattern(build_dir: str, pattern: str) -> list[str]:
    errors = []
    for html_file in sorted(
        glob.glob(f"{build_dir}/docs/**/index.html", recursive=True)
    ):
        content = open(html_file).read()
        if pattern in content:
            page = (
                html_file.replace(build_dir + "/", "")
                .replace("/index.html", "")
            )
            errors.append(f"  {page}")
    return errors


def check_unresolved_xrefs(build_dir: str) -> list[str]:
    xref_re = re.compile(r":(?:attr|class|meth|func|data|mod|obj):")
    errors = []
    for html_file in sorted(
        glob.glob(f"{build_dir}/docs/**/index.html", recursive=True)
    ):
        content = open(html_file).read()
        if xref_re.search(content):
            page = (
                html_file.replace(build_dir + "/", "")
                .replace("/index.html", "")
            )
            errors.append(f"  {page}")
    return errors


def main() -> int:
    build_dir = sys.argv[1] if len(sys.argv) > 1 else "website/build"
    failed = False

    checks = [
        ("Checking broken images", lambda: check_broken_images(build_dir)),
        (
            "Checking unresolved reST cross-references",
            lambda: check_unresolved_xrefs(build_dir),
        ),
        (
            "Checking missing code examples",
            lambda: check_pattern(build_dir, "Missing code example for"),
        ),
        (
            "Checking missing API entries",
            lambda: check_pattern(build_dir, "Missing API entry for"),
        ),
    ]

    for label, check_fn in checks:
        print(f"=== {label} ===")
        errors = check_fn()
        if errors:
            print(f"FAILED: {len(errors)} issues found:")
            print("\n".join(errors))
            failed = True
        else:
            print("OK")
        print()

    if failed:
        print("=== CHECKS FAILED ===")
        return 1
    else:
        print("=== All checks passed ===")
        return 0


if __name__ == "__main__":
    sys.exit(main())
