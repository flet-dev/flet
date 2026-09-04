"""Generate app icons and splash screens for every platform Flet builds for.

Rendering is separate from writing: :func:`render_icons` and
:func:`render_splash` are pure, taking images and returning images without
touching the filesystem or emitting log output, so a UI can preview results
before anything is built. :func:`write` is the only function that persists
anything.

Diagnostics are data. Anything worth telling the user lands in
:attr:`RenderResult.warnings` rather than being printed, so the caller decides
how to surface it.
"""

__all__ = []
