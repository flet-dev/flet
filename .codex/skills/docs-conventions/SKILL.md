---
name: docs-conventions
description: Use when writing or reviewing Flet documentation, including Python docstrings (Google style, reST roles, admonitions), Markdown docs (cross-references, images, code examples), and sidebar navigation.
---

# Documentation Conventions

## Python Docstrings

Use **Google style** docstrings with sections: `Args:`, `Returns:`, `Raises:`, `Note:`, `Example:`, `Warning:`.

### Cross-references (reST roles)

Use reST roles in Python docstrings. CrocoDocs renders them as links in the API docs.

**Supported roles:** `:class:`, `:attr:`, `:meth:`, `:func:`, `:data:`, `:mod:`

```python
"""
If a parent is a :class:`~flet.ResponsiveRow`, this property determines
how many virtual columns the control spans.

See :attr:`value` for the current selection.

Calls :meth:`~flet.Page.update` after modifying controls.
"""
```

**Rules:**

- **Qualified reference:** `:class:`flet.Page`` — links to Page, displays `flet.Page`
- **Short display with `~`:** `:class:`~flet.Page`` — links to Page, displays just `Page`
- **Local member (same class):** `:attr:`value`` — no qualifier needed
- **Method with parens:** `:meth:`update`` — do NOT include `()` in the target

**Not supported:**

- Custom labels like `:class:`my label <flet.Page>`` — the label is always auto-derived from the target
- Roles for symbols not in CrocoDocs API data degrade to inline code

### Admonitions in docstrings

Google-style section headers render as Docusaurus admonitions:

```python
"""
Note:
    Has effect only if the direct parent is a :class:`~flet.Column`.

Warning:
    This property is deprecated. Use :attr:`new_prop` instead.

Example:
    Setting up a basic layout:
    ``ft.Column(controls=[ft.Text("Hello")])``
"""
```

Supported kinds: `Note`, `Warning`, `Danger`, `Tip`, `Info`. Unsupported kinds (e.g. `Limitation`, `Example`) are normalized to `note`. Empty admonitions are skipped.

## Markdown Docs

Docs live in `website/docs/`. Docusaurus renders them as the website.

### Cross-references

Use relative `.md` paths with dot-format anchors:

```markdown
See [Page](../controls/page.md) for details.

The [route](../controls/page.md#flet.Page.route) property controls navigation.
```

Anchor format: `#flet.ClassName.member_name` (dots, not hyphens).

### Admonitions

```markdown
:::note
Basic note without title.
:::

:::warning[Important]
Warning with a custom title.
:::
```

Supported types: `note`, `info`, `tip`, `warning`, `danger`.

### Front matter

```yaml
---
class_name: "flet.Container"
examples: "controls/container"
example_images: "test-images/examples/material/golden/macos/container"
example_media: "examples/controls/container/media"
title: "Container"
---
```

- `examples` — root-relative path under `sdk/python/examples/`
- `example_images` / `example_media` — root-relative under `website/static/docs/`

### Images

Use the CrocoDocs `Image` component. Paths without `../` are resolved against `/docs/`:

```jsx
import {Image} from '@site/src/components/crocodocs';

<Image src={frontMatter.example_images + '/image_for_docs.png'} width="55%" />
```

For absolute paths (one-off assets in `static/`):

```jsx
<Image src="/docs/assets/controls/charts/bar-chart-diagram.svg" width="65%" />
```

### Code examples

```jsx
import {CodeExample} from '@site/src/components/crocodocs';

<CodeExample path={frontMatter.examples + '/example_1.py'} />
```

Paths are relative to the configured `examples_root` (`sdk/python/examples/`).

## Sidebar Navigation

Edit `website/sidebars.yml` to change navigation structure:

```yaml
docs:
  Getting started:
  - getting-started/installation.md
  Controls:
    _generated_index:
      title: Controls
      slug: /controls
      description: Browse the complete catalog of controls.
    AlertDialog: controls/alertdialog.md
```

After editing, regenerate `sidebars.js`:

```bash
cd website && yarn crocodocs:generate
```
