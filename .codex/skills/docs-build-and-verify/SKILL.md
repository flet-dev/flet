# Docs Build and Verification

## Prerequisites

Node.js 20 is required:

```bash
nvm use 20
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

`yarn build` automatically reports broken links and anchors. The build fails if any are found.

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
