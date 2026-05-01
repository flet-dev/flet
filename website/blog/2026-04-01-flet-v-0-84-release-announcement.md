---
slug: flet-v-0-84-release-announcement
title: "Flet 0.84.0: Goodbye MkDocs, hello CrocoDocs!"
authors: feodor
tags: [releases]
---

Flet 0.84.0 is a developer-experience release: new documentation website and re-worked examples.

Highlights in this release:

* Flet docs are back on Docusaurus - fast dev server, working hot reload, unified website.
* Meet CrocoDocs, our new tool that bridges Python docstrings and Docusaurus.
* All 466 Flet examples migrated to standalone projects with rich metadata for Gallery and AI discovery.

{/* truncate */}

## How to upgrade

If you use pip:

```bash
pip install 'flet[all]' --upgrade
```

If you use uv with `pyproject.toml` and want to upgrade everything:

```bash
uv sync --upgrade
```

If you want to upgrade only Flet packages:

```bash
uv sync --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web
```

## Goodbye, MkDocs! Hello, CrocoDocs!

The Flet website has always been built on [Docusaurus](https://docusaurus.io/) - it's fast, extensible, and has great MDX support. But we were authoring API docs manually, which caused synchronization issues with the source code and a lot of duplication: we'd write the same content in Python docstrings and then again in Docusaurus pages.

For Flet "v1", [@ndonkoHenri](https://github.com/ndonkoHenri) made a huge push by moving all API docs into Python docstrings and configuring [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) + [mkdocstrings](https://mkdocstrings.github.io/) to serve Flet documentation. It was a great and timely decision to make docstrings the single source of truth.

And it worked, but with some quirks:

* Flet has a large codebase with many cross-references. The docs dev server took **around 3 minutes** to start.
* For [some](https://github.com/mkdocs/mkdocs/issues/4032) [reason](https://github.com/squidfunk/mkdocs-material/issues/8478), hot reload was not working - which meant making a change, restarting, and waiting another 3 minutes to see the result!

Then, one day, we saw this warning in a build log and got a feeling that something was off:

:::warning
WARNING - MkDocs 2.0 is incompatible with Material for MkDocs
:::

Apparently, there is a [whole story](https://fpgmaas.com/blog/collapse-of-mkdocs/) that has been developing for a few years. The short version: the MkDocs original author started working on MkDocs 2.0 which drops plugin support and is not compatible with MkDocs 1.x. The Material for MkDocs team started working on [Zensical](https://zensical.io/), a MkDocs rewrite in Rust that is backward-compatible but launched with many plugins still missing.

We decided to bring docs back to Docusaurus - but this time with a tool that keeps docstrings as the single source of truth.

### Meet CrocoDocs

<img src="/img/blog/flet-0-84/crocodocs-logo.png" className="screenshot-40" />

CrocoDocs is our home-grown tool that transforms Flet API data into a form that Docusaurus can render. The idea is simple: extract API information from Python docstrings using [Griffe](https://mkdocstrings.github.io/griffe/), produce JSON data and MDX partials, and let Docusaurus render everything using custom MDX components and remark plugins.

The pipeline looks like this:

1. **Extract** - Griffe parses all Python packages and collects classes, functions, docstrings, and type annotations.
2. **Transform** - CrocoDocs builds an `api-data.json` with all API entries and a cross-reference map (`xref_map`) that resolves symbol names to documentation URLs.
3. **Generate** - MDX partials are produced for CLI docs, permissions, and the PyPI package index. Code examples are indexed from the examples directory.
4. **Render** - Docusaurus picks up the generated data and a custom remark plugin resolves cross-references into clickable links.

It's a modern Python project, managed with uv and configured entirely via `pyproject.toml`.

### New cross-reference format

We switched from [mkdocstrings-python-xref](https://analog-garage.github.io/mkdocstrings-python-xref/latest/) format to reST-style roles in docstrings. This was a deliberate choice: reST roles are a well-known standard, and - crucially - they are navigable in VS Code and other editors that render docstring tooltips.

Before (mkdocstrings):

```python
"""See [Page][flet.] and [Control.visible][flet.] for details."""
```

After (reST roles):

```python
"""See :class:`~flet.Page` and :attr:`flet.Control.visible` for details."""
```

The supported roles are `:class:`, `:attr:`, `:meth:`, `:func:`, `:mod:`, `:data:`, and `:obj:`. The `~` prefix shortens the display name - `:class:`~flet.Page`` renders as just "Page" while still linking to the full path.

Here's what it looks like in VS Code - docstring links are rendered and navigable right in the tooltip:

<img src="/img/blog/flet-0-84/vscode-docstring.png" className="screenshot-80 screenshot-rounded" />

### Strict CI checks

In addition to the broken-link checks that Docusaurus performs during build, we added a custom CI script with strict validation:

* **Broken images** - verifies that every `<img src="...">` points to an existing file.
* **Unresolved reST xrefs** - catches any `:class:`, `:attr:`, `:meth:` markers that were not resolved to links.
* **Missing code examples** - flags `<CodeExample>` components that reference non-existent example files.
* **Missing API entries** - detects symbols referenced in docs but absent from `api-data.json`.

If any check fails, the build fails. No broken docs make it to production.

### The results

The migration from MkDocs to Docusaurus brought exactly what we hoped for:

* The generate phase and Docusaurus dev server **start in a few seconds** (down from ~3 minutes).
* **Hot reload works.** Change a page, save, see the update.
* A **single unified website** for the landing page and docs, with a modern design.
* **Full-text search with Algolia.**
* A tool we own and can evolve as Flet grows.

CrocoDocs is not yet available on PyPI, but if you'd like to adopt it for your Python project - let me know!

More info:

* PR: [#6359](https://github.com/flet-dev/flet/pull/6359)

## Examples migrated to projects

Every Flet example is now a standalone project with its own `pyproject.toml` and rich metadata. Here's why we made this change:

**Better discovery.** Each project carries structured metadata - categories, description, keywords, a list of controls used, complexity level, and more. We need this data for building Gallery v2 (available on the website and as a Flet app) and for building the index for Flet MCP, so AI assistants can find the right example for you.

**Easier to build and run.** Previously, if you wanted to try an example, you'd copy it into your own project, figure out the dependencies, and wire things up. Now every example is a complete project you can clone and run directly with `flet run`.

**Self-contained.** Every project includes all its dependencies (`flet_charts`, `flet_map`, etc.), permissions, bundle IDs, and assets needed to successfully build and run on any platform.

### What a project looks like

Before - a flat Python file with no metadata:

```
sdk/python/examples/controls/
├── button_examples.py
├── canvas_examples.py
└── ...
```

After - a structured project directory:

```
sdk/python/examples/controls/
├── material/
│   └── button/
│       ├── basic/
│       │   ├── main.py
│       │   └── pyproject.toml
│       ├── icons/
│       │   ├── main.py
│       │   └── pyproject.toml
│       └── styling/
│           ├── main.py
│           └── pyproject.toml
├── core/
│   └── canvas/
│       ├── bezier_curves/
│       ├── brush/
│       └── ...
└── cupertino/
    └── cupertino_button/
        └── basic/
```

Each `pyproject.toml` includes Gallery and MCP metadata:

```toml
[project]
name = "button-basic"
version = "1.0.0"
description = "Basic enabled and disabled Button examples."
keywords = ["button", "material", "basic", "disabled"]
dependencies = ["flet"]

[tool.flet.gallery]
categories = ["Buttons/Button"]

[tool.flet.metadata]
title = "Basic button"
controls = ["SafeArea", "Column", "Button"]
layout_pattern = "inline-actions"
complexity = "basic"
features = ["enabled and disabled states"]
```

In total, **466 examples** were migrated to this format.

More info:

* PR: [#6355](https://github.com/flet-dev/flet/pull/6355)

## Conclusion

Flet 0.84.0 is about the ecosystem around the framework: better docs, better examples, better tooling. CrocoDocs gives us a documentation pipeline we can trust and evolve. Standalone example projects make every sample discoverable, runnable, and ready for AI-assisted workflows.

Try it and share feedback in [GitHub Discussions](https://github.com/flet-dev/flet/discussions) or on [Discord](https://discord.gg/dzWXP8SHG8).

Happy Flet-ing!
