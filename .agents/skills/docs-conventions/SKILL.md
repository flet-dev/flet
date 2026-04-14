---
name: docs-conventions
description: Use when writing or reviewing Flet documentation, including Python docstrings (Google style, reST roles, admonitions), Markdown docs (cross-references, images, code examples), and sidebar navigation.
---

# Documentation Conventions

Docs live in `website/docs/`. Docusaurus renders them as the website.

## Python Docstrings

Use **Google style** docstrings with sections: `Args:`, `Returns:`, `Raises:`, `Note:`, `Example:`, `Warning:`.

## Cross-references

### reST roles

Prefer these in Python docstrings. CrocoDocs renders them as links in
the API docs and they keep authoring terse when the auto-derived label is acceptable.

**Supported roles:** `:class:`, `:attr:`, `:meth:`, `:func:`, `:data:`, `:mod:`

```python
"""
If a parent is a :class:`~flet.ResponsiveRow`, this property determines
how many virtual columns the control spans.

See :attr:`value` or :attr:`flet.Text.size` for the current selection.

Calls :meth:`flet.Page.update` after modifying controls.
"""
```

**Rules:**

- **Qualified reference:** `:attr:`flet.Page.route`` — links to the member, displays inline code `Page.route`
- **Short display with `~`:** `:attr:`~flet.Page.route`` — links to the member, displays inline code `route`
- **Local member (same class):** `:attr:`value`` — no qualifier needed
- **Method with parens:** `:meth:`update`` — do NOT include `()` in the target

For plain class references like `:class:`flet.Page``, the website strips the leading `flet.`
automatically, so both `:class:`flet.Page`` and `:class:`~flet.Page`` display as inline code `Page`.

**Not supported:**

- Custom labels like `:class:`my label <flet.Page>`` — the label is always auto-derived from the target
- Roles for symbols not in CrocoDocs API data degrade to inline code

### Markdown links

Use this syntax when the displayed text must differ from the symbol target or when
explicitly required by user. This is especially useful in docs-only strings such as the
`docs_reason` parameter of `@deprecated`, extracted validation messages, or short admonition text
where you want:

- inline-code labels with punctuation, such as `new_func()` or `local_position.x`,
- plain-language labels that do not match the target exactly,
- explicit full targets in the link destination for clarity.

Use relative `.md` paths with dot-format anchors.

Examples:

```markdown
Control: [`Page`](../controls/page.md)
Type: [`DragTargetEvent.global_position`](../types/dragtargetevent.md#flet.DragTargetEvent.global_position)
Plain text: [route](../controls/page.md#flet.Page.route)
Method: [`Page.update()`](../controls/page.md#flet.Page.update)
```

## Admonitions in docstrings

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

Supported kinds: `Note`, `Warning`, `Danger`, `Tip`, `Info`.
Unsupported kinds (e.g. `Limitation`, `Example`) are normalized to `note`.
Empty admonitions are skipped.

## Admonitions

```markdown
:::note
Basic note without title.
:::

:::warning[Important]
Warning with a custom title.
:::
```

Supported types: `note`, `info`, `tip`, `warning`, `danger`.

## Front matter

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

## Images

Use the CrocoDocs `Image` component. Paths without `../` are resolved against `/docs/`:

```jsx
import {Image} from '@site/src/components/crocodocs';

<Image src={frontMatter.example_images + '/image_for_docs.png'} width="55%" />
```

For absolute paths (one-off assets in `static/`):

```jsx
<Image src="/docs/assets/controls/charts/bar-chart-diagram.svg" width="65%" />
```

## Code examples

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
