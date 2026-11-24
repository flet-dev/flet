---
name: test-flet-apps-dev
description: Use when testing or debugging Flet apps in maintainer/contributor development mode with local Python package sources and the local Flutter client, including web, desktop, browser, and computer-use verification workflows.
---

# Test Flet Apps In Dev Mode

Use this skill when validating a Flet app, example, feature, or bug fix against
this repo's local Python packages and/or local Flutter client during maintainer
or contributor work.

## Core model

Flet dev-mode testing usually has one or two processes:

1. A Python Flet app/server, run from `sdk/python`.
2. The local Flutter client, run from `client`, when Dart/client or extension code
   must be tested.

If only Python code changed, `uv run flet run ...` is often enough. If Dart,
Flutter, extension, or transport code changed, run the local Flutter client so
the changed Dart code is actually used.

The local Flutter client debug build uses a fixed app-server URL from
`client/lib/main.dart`:

```dart
if (kDebugMode) {
  pageUrl = "http://localhost:8550";
}
```

Therefore, when using the local Flutter client without extra URL arguments,
start the Python app on port `8550`.

## Start the Python app

Run from `{repo}/sdk/python`:

```bash
uv run flet run -w -p 8550 examples/controls/core/interactive_viewer/handling_events/main.py
```

Adjust the sample path as needed. Use port `8550` when the local Flutter client
will connect with its default debug URL. Keep this process running and watch its
stdout for Python callback output, tracebacks, and event payloads.

For web-only checks with the packaged web client, open:

```text
http://127.0.0.1:8550
```

## Run the local Flutter client

Run these from `{repo}/client`.

### Desktop

Use when validating native desktop behavior on the current host OS:

```bash
fvm flutter run -d macos     # macOS
fvm flutter run -d windows   # Windows
fvm flutter run -d linux     # Linux
```

The debug client defaults to `http://localhost:8550` when no app URL argument is
provided. Use the platform target that exists on the current machine. Use
Computer Use or the relevant platform automation to navigate and interact with
the app window.

### Flutter web in Chrome

Use when Dart web behavior must be validated in Flutter's default web debug
browser:

```bash
fvm flutter run -d chrome
```

This opens a fresh browser connected to the Python app server on port `8550`.

### Flutter web in another Chromium browser

If the requested browser is not listed by `flutter devices`, prefer the web
server target and open the served URL in that browser:

```bash
fvm flutter run -d web-server --web-hostname 127.0.0.1 --web-port 8660
open -a "Brave Browser" http://127.0.0.1:8660
```

Using `CHROME_EXECUTABLE` can work, but Flutter may fail to attach its debug
websocket in non-default Chromium browsers. Fall back to `web-server` if that
happens.

## Browser and UI interaction

- For local browser targets (`localhost`, `127.0.0.1`, `file://`), prefer the
  in-app browser or the Browser Use plugin when explicitly requested.
- Use Computer Use for native desktop apps and external browsers when browser
  MCP is not the requested tool or cannot control that browser.
- For chart/canvas-heavy UI, click/hover coordinates may be necessary because
  accessibility trees often expose only the HTML canvas container.

## Reading evidence

Always inspect both sides:

- Python app stdout: event payloads, user `print()` calls, Python tracebacks.
- Flutter run stdout: client-side event payloads, WebSocket messages, Flutter
  exceptions, hot reload/restart status.
- Browser/app state: the actual rendered UI and any visible error banner.

For client/server protocol bugs, compare the raw outgoing Dart event in Flutter
logs with the decoded Python event object in Python logs.

## Hot reload and restart

For Flutter client sessions:

- Press `r` for hot reload after many Dart-only edits.
- Press `R` for hot restart if state, initialization, or extension registration
  may be stale.
- Quit with `q` before final response unless the user explicitly wants the app
  left running.
- Press `h` for help on other Flutter run key commands.

For Python app sessions, restart `uv run flet run ...` after Python source or
sample changes if the running process does not pick them up.

## Troubleshooting

- If a sandboxed Flutter command fails trying to write FVM or Flutter cache files
  such as `engine.stamp`, rerun the same command with escalation.
- If `flutter devices` does not list Brave/Edge/etc., use `flutter run -d web-server`
  and open the URL in the target browser.
- If the UI shows a generic Flet error banner, check Python stdout first; the
  root cause is often a handler exception.
- If an event handler indexes a list payload, confirm the empty-list case before
  treating it as a framework bug.
- If the local Flutter client cannot connect, confirm the Python app is running
  on port `8550` or pass an explicit app URL when the client path supports it.

## Finish checklist

- Stop long-running app/test sessions unless asked to leave them running.
- State exactly which surfaces were tested: packaged web, local Flutter web,
  desktop target, target browser, or sample-only.
- Include the key observed payload/error before and after the fix.
- Separate framework bugs from sample-code guard issues.
