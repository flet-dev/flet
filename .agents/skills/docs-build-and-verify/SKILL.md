---
name: docs-build-and-verify
description: Use when asked to build, preview, or verify the Flet documentation website, including checking for broken links, broken images, and unresolved reST cross-references.
---

# Docs Build and Verification

## Prerequisites

Node.js 24 is required, matching what CI runs:

```bash
nvm use 24
```

## Build

Full production build (includes broken link detection):

```bash
cd website && yarn build
```

Dev server with hot reload:

```bash
cd website && yarn start
```

Regenerate API data and sidebars only (no Docusaurus build):

```bash
cd website && yarn crocodocs:generate
```

## Check Broken Links

`yarn build` reports both, but only broken *links* fail the build. Docusaurus defaults
`onBrokenAnchors` to `warn` and `docusaurus.config.js` does not override it, so a broken
anchor scrolls past in the log and still ships - grep the build output for `Broken anchor`
rather than trusting the exit code.

## Check Broken Images

Run this after `yarn build` to find images referenced in HTML that don't exist:

```bash
cd website && python3 -c "
import re, os, glob

build_dir = 'build'
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
else:
    print('No broken images found!')
"
```

## Check Unresolved reST Cross-References

After building, check for reST roles that failed to resolve and appear as raw text:

```bash
cd website && grep -r ':attr:\|:class:\|:meth:\|:func:' build/docs/ --include='*.html' -l
```

If any files are listed, those pages have unresolved cross-references that render as plain text instead of links.
