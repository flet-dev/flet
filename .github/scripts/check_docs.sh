#!/usr/bin/env bash
set -euo pipefail

BUILD_DIR="${1:-website/build}"

echo "=== Checking broken images ==="
broken_images=$(python3 -c "
import re, os, glob

build_dir = '$BUILD_DIR'
img_re = re.compile(r'<img[^>]+src=\"(/[^\"]+)\"', re.IGNORECASE)
broken = []

for html_file in sorted(glob.glob(f'{build_dir}/docs/**/index.html', recursive=True)):
    page = html_file.replace(build_dir + '/', '').replace('/index.html', '')
    content = open(html_file).read()
    for match in img_re.finditer(content):
        src = match.group(1)
        if src.startswith('http') or src.startswith('data:'):
            continue
        file_path = os.path.join(build_dir, src.lstrip('/'))
        if not os.path.exists(file_path):
            broken.append((page, src))

if broken:
    print(f'Found {len(broken)} broken images:')
    for page, src in broken:
        print(f'  {page}: {src}')
    exit(1)
else:
    print('No broken images found.')
")

echo "=== Checking unresolved reST cross-references ==="
if grep -rl ':attr:\|:class:\|:meth:\|:func:' "$BUILD_DIR/docs/" --include='*.html' 2>/dev/null; then
    echo "ERROR: Found pages with unresolved reST cross-references (listed above)."
    exit 1
else
    echo "No unresolved reST cross-references found."
fi

echo "=== Checking missing code examples ==="
if grep -rl 'Missing code example for' "$BUILD_DIR/docs/" --include='*.html' 2>/dev/null; then
    echo "ERROR: Found pages with missing code examples (listed above)."
    exit 1
else
    echo "No missing code examples found."
fi

echo "=== Checking missing API entries ==="
if grep -rl 'Missing API entry for' "$BUILD_DIR/docs/" --include='*.html' 2>/dev/null; then
    echo "ERROR: Found pages with missing API entries (listed above)."
    exit 1
else
    echo "No missing API entries found."
fi

echo "=== All checks passed ==="
