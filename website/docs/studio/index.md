---
title: "Introduction"
---

# Flet Studio

[Flet Studio](https://flet.app) is a browser-based editor for writing, running, saving and
sharing Flet apps. Your Python code runs entirely in the browser via
[Pyodide](https://pyodide.org/) — there is no Flet account required to try it, and no
local install required to run something someone else built and shared with you.

## Why it exists

Flet Studio started as a tool we wanted for ourselves and kept being useful for things
we hadn't planned. In rough order:

- **A playground that saves your work.** Unlike a transient REPL or a paste-and-run
  sandbox, projects in Studio persist across sessions and across devices once you sign in.
- **A way to share small apps via a link.** Send a colleague or someone on the Flet team a
  URL and they can open, run, and read the code without setting anything up. Handy for
  bug reports, design sketches, and "look at this control".
- **A gallery of Flet examples that you can actually edit.** Browse examples, open one,
  tweak it, fork it into your own project — same editor, same runtime.
- **A zero-commitment way to try Flet.** Before `pip install flet`, before reading the
  getting-started docs, you can write a few lines and see them run.
- **A dogfooding project.** Studio's UI is itself a Flet app. Building it surfaces gaps
  in Flet and ideas for improvements, which feed back into the framework.
- **The base UI for future Flet services.** Cloud packaging and publishing are on the
  roadmap — Studio is the surface those will plug into. (Today: editor only.)

## How it works

- **Your code runs in the browser.** Flet Studio uses [Pyodide](https://pyodide.org/) —
  CPython compiled to WebAssembly — to execute your Python directly in the browser tab.
  Nothing you write is sent to a server to be run.
- **There is a Flet Studio backend, but it's only for the IDE itself** — file storage,
  authentication, accounts, project metadata. Your app's Python code never executes on
  our servers; it executes client-side, in your browser, in Pyodide.
- **The rendering engine is the same one `flet publish` and `flet build web` produce.**
  What you see in Studio is what you'd get from a published Flet static site — same
  controls, same layout, same web runtime.

## Limitations

Studio inherits the constraints of running Python in the browser. Most of these are
covered in more detail in the
[static website publishing docs](../publish/web/static-website/index.md):

- **Pure-Python packages and Pyodide-built wheels only.** Most of the Python ecosystem
  works, but packages with C/Rust extensions need a Pyodide build. See the
  [Pyodide built-in packages list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).
  Source-only sdists (no wheel) cannot be installed.
- **Single browser thread.** No real threads. Long blocking work freezes the UI — prefer
  async I/O.
- **Browser sandbox.** No access to your local filesystem, no shell, no access to local
  hardware that isn't exposed by the browser.
- **Performance.** Pyodide is roughly 3×–5× slower than CPython for CPU-bound code.
- **Cold start.** The first load fetches the Python runtime and any wheels you import,
  so initial load is slower than a native install. Subsequent loads are cached.

## Does it replace local Flet development?

No.

Studio is for trying Flet, prototyping small apps, sharing snippets, learning, and
showing off ideas. For everything else — desktop and mobile builds, native packages,
real multi-file projects, your favorite IDE and debugger, the full Python ecosystem
without the Pyodide constraints above — install Flet locally and use `flet run` and
`flet build`. See [installation](../getting-started/installation.md) when you're ready
to make the jump.
