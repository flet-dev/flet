---
title: "Introduction"
---

# Flet Studio

[Flet Studio](https://studio.flet.dev) is a browser-based workspace for building
Flet apps in Python. Write code yourself or work with an AI agent, run your app
alongside the editor, and share it with a link. No local installation is required.

## Highlights

- **AI-assisted development.** Describe an app, ask for a feature, or get help
  fixing a bug. The agent can read and edit project files, and its activity list
  shows code changes as inline diffs. Choose between Pro and Expert agents based
  on the access available to your account.
- **A browser IDE.** Edit Python, manage files in multi-file projects, and restore
  previous versions. Sign in to save your projects and access them across devices.
- **Live preview.** Run your app next to the editor and try out changes as you
  build, without setting up Python or Flutter on your machine.
- **Examples you can make your own.** Browse the
  [gallery](https://studio.flet.dev/gallery) of 500+ examples, templates, and apps.
  Open an example, fork it, and adapt it to your idea.
- **Sharing and private projects.** Share public apps with a link so others can
  run them and explore the code. Creator includes unlimited public and private
  apps; existing private apps on Explorer remain available.
- **Plans that fit your work.** Start with Explorer for free, or choose Creator
  for more monthly AI credits, Expert agent access, credit top-ups, and direct
  Flet support. Creator offers monthly and annual billing. See [pricing](/pricing)
  for plan details and how AI credits work.
- **Cloud packaging and publishing — coming soon.** Build app packages and
  publish them from Studio without a local build environment.

See [what's new](whats-new.md) for the latest improvements.

## How it works

1. **Start with an idea or an example.** Open Studio to try Flet, or browse the
   gallery and open an app. Sign in to save your own work and use AI assistance.
2. **Write code or ask the agent.** Edit project files directly, or describe what
   you want the AI agent to build or change. Review its edits and iterate with
   follow-up instructions.
3. **Run and check your app.** The preview runs your Python code in the browser
   using [Pyodide](https://pyodide.org/), a version of CPython compiled to
   WebAssembly. Test the result alongside your code and make further changes.
4. **Save, revisit, and share.** Keep working on your saved project, restore an
   earlier version when needed, or share a public app's link with others.

### Where your code runs

Your app's Python code executes in the browser, not on Flet Studio's servers.
It uses the same browser-based Flet runtime as a
[published static Flet website](../publish/web/static-website/index.md).

Studio's hosted services handle accounts, project files, version history, billing,
and AI assistance. When you use the AI agent, your prompts, conversation history,
and relevant project context are sent to AI model providers to generate a
response. Running an app preview and using the AI agent are separate operations;
browser-based execution does not mean all project data stays on your device.
See the [Privacy Policy](privacy-policy.md) for details.

## Frequently asked questions

### Do I need an account or a paid plan?

You can try Studio and run shared public apps without an account. Sign in to save
projects and use the AI agent. Explorer is free and includes monthly AI credits
and access to the Pro agent. Creator adds private apps, more credits, Expert agent
access, and on-demand credit top-ups. Accounts with an existing wallet credit
balance can also access Expert. See [pricing](/pricing) for current allowances.

### Do I have to use AI?

No. You can write and edit Python yourself, run your app, and use Studio's project
and sharing tools without asking the AI agent. AI credits are used when you run
the agent, not when you manually edit code or run an app preview.

<a id="limitations"></a>

### What are the limitations?

Studio's app preview inherits the constraints of running Python in the browser:

- **Package compatibility.** Pure-Python wheels and packages built for Pyodide
  are supported. Packages with C or Rust extensions need a compatible Pyodide
  build; source-only packages without a wheel cannot be installed in the browser.
  See the [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).
- **Single-threaded execution.** Long-running CPU work and blocking calls can
  freeze the UI. Prefer async I/O, or run heavy work on a server and call it
  through an API.
- **Browser sandbox.** Apps do not have unrestricted access to your local
  filesystem, a shell, or hardware. Access depends on the APIs and permissions
  available in the browser.
- **Performance and startup.** CPU-heavy work can be slower than local Python.
  The first load downloads the Python runtime and app dependencies; browser
  caching can speed up later loads.

See the [static website publishing guide](../publish/web/static-website/index.md)
for more on the browser runtime and package compatibility.

### Does it replace local Flet development?

Studio and local development complement each other. Studio provides an accessible
workspace for learning, prototyping, and building apps with multiple files,
AI assistance, and shareable previews.

Use local development when you need a native desktop or mobile runtime, packages
that do not work with Pyodide, local tools and hardware, or your preferred IDE and
debugger. Cloud packaging and publishing in Studio are still coming soon; for
now, use `flet run` and `flet build` locally for those workflows. See
[installation](../getting-started/installation.md) to get started.

The Flet framework is free and open source. You do not need a paid Studio plan to
develop or package Flet apps locally.
