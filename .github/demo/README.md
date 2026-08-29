# Linux icon demo

**This directory exists only on `test/fix-build-linux-icon` and is never
merged.** The branch is `fix/build-linux-icon` plus this directory and
[`../workflows/linux-icon-demo.yml`](../workflows/linux-icon-demo.yml).

Reviewing [#2269](https://github.com/flet-dev/flet/issues/2269) otherwise means
installing a Linux toolchain, building an app and running a packaging recipe by
hand, on a desktop session — none of which a diff can show. So CI does it, and
the run's artifacts are a `.deb` and an AppImage for x64 and arm64 that anyone
can download and open.

```
app/                   the demo app, built by the workflow
make_icon.py           regenerates app/src/assets/icon_linux.png
extract_recipe.py      pulls a packaging recipe out of the published docs
assert_bundle.py       checks what `flet build linux` produced
assert_packages.py     checks what the recipes produced
assert_runtime.sh      reads WM_CLASS and _NET_WM_ICON off the running app
HOW-TO.md             shipped inside each artifact, for whoever downloads it
```

## Why the recipes are not committed here

`website/docs/publish/linux.md` is the only copy. `extract_recipe.py` reads the
`.deb` and AppImage scripts out of that page and applies exactly the edits the
page tells a reader to make — the variables at the top — so a green run means
the *documented* recipes work, and the artifacts are what a reader following
them would get. A committed copy would drift from the page and prove nothing
about it.

Renaming a variable in the docs fails the run rather than silently packaging
`my_app`, because an override key that no longer matches is an error.

## The other workflows

`ci.yml`, `flet-test.yml`, `flet-build-test.yml` and
`macos-integration-tests.yml` each exclude this branch by name in their push
trigger, so a push here runs the demo and nothing else. Those exclusions are
part of the branch, and go away with it.
