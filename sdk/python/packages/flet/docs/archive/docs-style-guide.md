# Docs Guide

We make use of [mkdocs-material](https://squidfunk.github.io/mkdocs-material/reference/), [mkdocstrings-python](https://mkdocstrings.github.io/python/) and their extensions.

## Docstring Style

We use the google style for documentation. More info and examples [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

## Cross References

The class must be present in our topmost `__init__.py`, and can then be (cross-)referenced from anywhere as follows:
```
[`Row`][flet.Row]
[`Row.controls`][flet.Row.controls]
```

**The type of a property or its default value should not be mentioned in the docstring, as they are already described 
in their respective definitions, and made visible to the user by our docs engine.**

## Admonition

### Method 1

[Docs](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/)

```
/// admonition | Deprecated
    type: danger
Message.
///
```

`type` can be: 'note' (default), 'attention', 'caution', 'danger', 'error', 'tip', 'hint', 'warning'
 ([Visual example](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types))

 ### Method 2

[Docs](https://mkdocstrings.github.io/griffe/reference/docstrings/#google-syntax)

```
Note:
    Message.
```

Where `Note` can literally be replaced by anything, which will then be used as title of the Detail. 

However, for appropriate icons/colors, use predefined types, such as 'Note' (default), 'Attention', 'Caution', 'Danger', 'Error', 'Tip', 'Hint', 'Warning' ([Visual example](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types))

To specify a custom title:
```
Danger: My Custom Title
    Message.
```

## Details

[Docs](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/details/)

```
/// details | Deprecated
    type: danger
Message.
///
```

`type` can be: 'note' (default), 'attention', 'caution', 'danger', 'error', 'tip', 'hint', 'warning'
 ([Visual example](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types))

## Tabs

[Docs](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/tab/)

```
/// tab | Tab 1 title
Tab 1 content
///

/// tab | Tab 2 title
Tab 2 content
///
```

## Code

[Docs](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/)

## Images

[Docs](https://blueswen.github.io/mkdocs-glightbox/)

[Caption Docs](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/caption/)

```
![xyz](...)
/// caption
This is the caption of this image. It is optional.
///
```

Images are usually not centered when displayed. A hack to quickly center an image is to have add a caption block below it. It must not contain text.

