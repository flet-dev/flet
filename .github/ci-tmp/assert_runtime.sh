#!/usr/bin/env bash
# TEMPORARY -- part of the issue #2269 Linux icon verification harness.
#
# Launch the built app under Xvfb and read back the two X11 properties the
# fix is supposed to set:
#   WM_CLASS      -- proves g_set_prgname(APPLICATION_ID) took effect
#   _NET_WM_ICON  -- proves the window icon was loaded AND survived GDK's
#                    256 KiB property cap (oversized icons are dropped
#                    silently, which is the bug this harness exists to catch)
#
# Both properties are set during gtk_widget_realize(), which the runner does
# before the window is ever shown, so no window manager is needed.
#
# Usage: assert_runtime.sh <expected_wm_class> <expected_icon_size> <app_binary>
#        expected_icon_size is "WxH", e.g. "256x256"
set -uo pipefail

EXPECTED_CLASS="$1"
EXPECTED_ICON="$2"
APP_BIN="$3"

LOG="${RUNNER_TEMP:-/tmp}/app-runtime.log"

echo "== launching $APP_BIN under ${DISPLAY:-<no DISPLAY>}"
"$APP_BIN" > "$LOG" 2>&1 &
APP_PID=$!
trap 'kill "$APP_PID" 2>/dev/null || true' EXIT

# Wait for a mapped-or-unmapped toplevel carrying our class. GDK also creates
# an InputOnly group-leader window with the same class, so those are skipped.
WIN=""
for _ in $(seq 1 90); do
  if ! kill -0 "$APP_PID" 2>/dev/null; then
    echo "!! app exited early; last 40 log lines:" >&2
    tail -40 "$LOG" >&2
    exit 1
  fi
  for candidate in $(xwininfo -root -children 2>/dev/null \
      | grep -oE '0x[0-9a-f]+'); do
    if xwininfo -id "$candidate" 2>/dev/null | grep -q "Class: InputOnly"; then
      continue
    fi
    if xprop -id "$candidate" WM_CLASS 2>/dev/null | grep -q "$EXPECTED_CLASS"; then
      WIN="$candidate"
      break 2
    fi
  done
  sleep 1
done

if [ -z "$WIN" ]; then
  echo "!! no window with WM_CLASS containing '$EXPECTED_CLASS' appeared" >&2
  echo "-- window tree:" >&2
  xwininfo -root -children 2>&1 | head -40 >&2
  echo "-- app log:" >&2
  tail -40 "$LOG" >&2
  exit 1
fi

echo "== found window $WIN"
WM_CLASS="$(xprop -id "$WIN" WM_CLASS 2>/dev/null)"
echo "   $WM_CLASS"

status=0
if echo "$WM_CLASS" | grep -q "\"$EXPECTED_CLASS\""; then
  echo "  PASS  WM_CLASS is the bundle id (g_set_prgname took effect)"
else
  echo "  FAIL  WM_CLASS is not '$EXPECTED_CLASS'"
  status=1
fi

# xprop prints _NET_WM_ICON as a CARDINAL list whose first two values are the
# width and height of the first icon.
ICON_RAW="$(xprop -id "$WIN" _NET_WM_ICON 2>/dev/null || true)"
if echo "$ICON_RAW" | grep -q "not found"; then
  echo "  FAIL  _NET_WM_ICON is absent -- GDK dropped the icon (too large?)"
  status=1
else
  DIMS="$(echo "$ICON_RAW" | tr ',' '\n' | grep -oE '[0-9]+' | head -2 | paste -sd 'x' -)"
  if [ "$DIMS" = "$EXPECTED_ICON" ]; then
    echo "  PASS  _NET_WM_ICON is set at $DIMS"
  else
    echo "  FAIL  _NET_WM_ICON is $DIMS, expected $EXPECTED_ICON"
    status=1
  fi
fi

kill "$APP_PID" 2>/dev/null || true
exit "$status"
