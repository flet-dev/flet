import pytest

import flet as ft
import flet.testing as ftt

sample1 = """
# Markdown Example
Markdown allows you to easily include formatted text, images, and even formatted Dart
code in your app.

## Titles

Setext-style

This is an H1
=============

This is an H2
-------------

Atx-style

# This is an H1

## This is an H2

###### This is an H6

Select the valid headers:

- [x] `# hello`
- [ ] `#hello`

## Links

[inline-style](https://www.google.com)

## Styling

Style text as _italic_, __bold__, ~~strikethrough~~, or `inline code`.

- Use bulleted lists
- To better clarify
- Your points


"""

sample2 = """
## Tables

|Syntax                                 |Result                               |
|---------------------------------------|-------------------------------------|
|`*italic 1*`                           |*italic 1*                           |
|`_italic 2_`                           | _italic 2_                          |
|`**bold 1**`                           |**bold 1**                           |
|`__bold 2__`                           |__bold 2__                           |
|`This is a ~~strikethrough~~`          |This is a ~~strikethrough~~          |
|`***italic bold 1***`                  |***italic bold 1***                  |
|`___italic bold 2___`                  |___italic bold 2___                  |
|`***~~italic bold strikethrough 1~~***`|***~~italic bold strikethrough 1~~***|
|`~~***italic bold strikethrough 2***~~`|~~***italic bold strikethrough 2***~~|


## Code blocks

Formatted Dart code looks really pretty too:

```
void main() {
  runApp(MaterialApp(
    home: Scaffold(
      body: ft.Markdown(data: markdownData),
    ),
  ));
}
```
"""

md = ft.Markdown(
    selectable=True,
    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
)


@pytest.mark.asyncio(loop_scope="module")
async def test_md_1(flet_app: ftt.FletTestApp, request):
    md.value = sample1
    await flet_app.assert_control_screenshot(
        request.node.name,
        md,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_md_2(flet_app: ftt.FletTestApp, request):
    md.value = sample2
    await flet_app.assert_control_screenshot(
        request.node.name,
        md,
    )
