---
slug: standalone-flet-web-apps-with-pyodide
title: Standalone Flet web apps with Pyodide
authors: feodor
tags: [releases]
---

import Card from '@site/src/components/card';

We've just released [Flet 0.4.0](https://pypi.org/project/flet/) with a super exciting new feature - [packaging Flet apps into a standalone static website](https://docs.flet.dev/publish/web/static-website/) that can be run entirely in the browser! The app can be published to any free hosting for static websites such as GitHub Pages or Cloudflare Pages. Thanks to [Pyodide](https://pyodide.org/en/stable/) - a Python port to WebAssembly!

<img src="/img/blog/pyodide/pyodide-logo.png" className="screenshot-50" />

You can quickly build awesome single-page applications (SPA) entirely in Python and host them everywhere! No HTML, CSS or JavaScript required!

<!-- truncate -->

## Quick Flet with Pyodide demo

Install the latest Flet package:

```
pip install flet --upgrade
```

Create a simple `counter.py` app:

```python title="counter.py"
import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.run(main)
```

Run a brand-new `flet publish` command to publish Flet app as a static website:

```
flet publish counter.py
```

The website will be published to `dist` directory next to `counter.py`.
Give website a try using built-in Python web server:

```
python -m http.server --directory dist
```

Open `http://localhost:8000` in your browser to check the published app.

<img src="/img/docs/getting-started/flet-counter-safari.png" className="screenshot-50" />

Here are a few live Flet apps hosted at Cloudflare Pages:

export const ImageCard = ({title, href, imageUrl}) => (
    <div className="col col--4 margin-bottom--lg">
      <Card href={href}>
        <img src={"/img/gallery/" + imageUrl} className="screenshot-100"/>
        <h2>{title}</h2>
      </Card>
    </div>
);

<div className="margin-top--lg">
  <section className="row">
    <ImageCard title="To-Do" href="https://gallery.flet.dev/todo/" imageUrl="todo.png" />
    <ImageCard title="Icons browser" href="https://gallery.flet.dev/icons-browser/" imageUrl="icons-browser.png" />
    <ImageCard title="Calc" href="https://gallery.flet.dev/calculator/" imageUrl="calc.png" />
    <ImageCard title="Solitaire" href="https://gallery.flet.dev/solitaire/" imageUrl="solitaire.png" />
    <ImageCard title="Trolli" href="https://gallery.flet.dev/trolli/" imageUrl="trolli.png" />
  </section>
</div>

[Check the guide](https://docs.flet.dev/publish/web/static-website/) for more information about publishing Flet apps as standalone websites.

## Built-in Fletd server in Python

Flet 0.4.0 also implements a [new Flet desktop architecture](https://flet.dev/blog/flet-mobile-update#flet-new-desktop-architecture).

It replaces Fletd server written in Go with a light-weight shim written in Python with a number of pros:

1. Only 2 system processes are needed to run Flet app: Python interpreter and Flutter client.
2. Less communication overhead (minus two network hops between Python and Fletd) and lower latency (shim uses TCP on Windows and Unix domain sockets on macOS/Linux).
3. Shim binds to `127.0.0.1` on Windows by default which is more secure.
4. The size of a standalone app bundle produced by `flet pack` reduced by ~8 MB.

The implementation was also required to support Pyodide (we can't run Go web server in the browser, right?) and paves the way to iOS and Android support.

### Other changes

* All controls loading resources from web URLs (`Image.src`, `Audio.src`, `Page.fonts`, `Container.image_src`) are now able to load them from local files too, by providing a full path in the file system, and from `assets` directory by providing relative path. For desktop apps a path in `src` property could be one of the following:
  * A path relative to `assets` directory, with or without starting slash, for example: `/image.png` or `image.png`. The name of artifact dir should not be included.
  * An absolute path within a computer file system, e.g. `C:\projects\app\assets\image.png` or `/Users/john/images/picture.png`.
  * A full URL, e.g. `https://mysite.com/images/pic.png`.
  * Add `page.on_error = lambda e: print("Page error:", e.data)` to see failing images.
* `flet` Python package has separated into two packages: `flet-core` and `flet`.
* PDM replaced with Poetry.
* `beartype` removed everywhere.

### 💥 Breaking changes

* Default routing scheme changed from "hash" to "path" (no `/#/` at the end of app URL). Use `ft.run(main, route_url_strategy="hash")` to get original behavior.
* OAuth authentication is not supported anymore in standalone desktop Flet apps.

## Async support

Flet apps can now be written as async apps and use `asyncio` with other Python async libraries. Calling coroutines is naturally supported in Flet, so you don't need to wrap them to run synchronously.

To start with an async Flet app you should make `main()` method `async`:

```python
import flet as ft

async def main(page: ft.Page):
    await page.add_async(ft.Text("Hello, async world!"))

ft.run(main)
```

[Read the guide](https://docs.flet.dev/cookbook/async-apps/) for more information about writing async Flet apps.

## Conclusion

Flet 0.4.0 brings the following exciting features:

- Standalone web apps with Pyodide running in the browser and hosted on a cheap hosting.
- Faster and more secure architecture with a built-in Fletd server.
- Async apps support.

Upgrade Flet module to the latest version (`pip install flet --upgrade`), give `flet publish` command a try and [let us know](https://discord.gg/dzWXP8SHG8) what you think!

Hey, by the way, [Flet project](https://github.com/flet-dev/flet) has reached ⭐️ 4.2K stars ⭐️ (+1K in just one month) - keep going! 