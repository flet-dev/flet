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
# Every X call is individually bounded and the whole search runs against a
# wall-clock deadline: a headless runner is exactly where these hang, and a
# hang here used to stall the job for minutes with nothing to show for it.
# Whatever happens, the window tree is dumped before exiting.
#
# Usage: assert_runtime.sh <expected_wm_class> <expected_icon_size> <app_binary>
#        expected_icon_size is "WxH", e.g. "256x256"
set -uo pipefail

EXPECTED_CLASS="$1"
EXPECTED_ICON="$2"
APP_BIN="$3"

LOG="${RUNNER_TEMP:-/tmp}/app-runtime.log"
DEADLINE_SECS=60

x() { timeout 5s "$@" 2>/dev/null; }

dump_tree() {
  echo "-- window tree:"
  x xwininfo -root -children | head -30
  echo "-- app log (tail):"
  tail -25 "$LOG" 2>/dev/null || echo "   (no log)"
}

echo "== launching $APP_BIN under ${DISPLAY:-<no DISPLAY>}"
# setsid puts the app in its own process group: a Flet app forks a bundled
# Python child, and killing only the parent leaves that child alive holding
# the display, which keeps xvfb-run (and therefore the CI step) from ever
# returning.
setsid "$APP_BIN" > "$LOG" 2>&1 &
APP_PID=$!

cleanup() {
  kill -TERM -- "-${APP_PID}" 2>/dev/null || kill -TERM "${APP_PID}" 2>/dev/null || true
  for _ in 1 2 3; do
    kill -0 "${APP_PID}" 2>/dev/null || return 0
    sleep 1
  done
  kill -KILL -- "-${APP_PID}" 2>/dev/null || kill -KILL "${APP_PID}" 2>/dev/null || true
}
trap cleanup EXIT

# Collect every window whose WM_CLASS matches, then prefer one that actually
# carries an icon: GDK also creates an InputOnly group-leader window with the
# same class, and that one never has _NET_WM_ICON.
WIN=""
ICON_WIN=""
END=$((SECONDS + DEADLINE_SECS))
while [ "$SECONDS" -lt "$END" ]; do
  if ! kill -0 "$APP_PID" 2>/dev/null; then
    echo "!! app exited early" >&2
    dump_tree >&2
    exit 1
  fi
  for id in $(x xwininfo -root -children | grep -oE '0x[0-9a-f]+'); do
    if x xprop -id "$id" WM_CLASS | grep -q "\"${EXPECTED_CLASS}\""; then
      WIN="$id"
      if x xprop -id "$id" _NET_WM_ICON | grep -qv "not found"; then
        ICON_WIN="$id"
        break
      fi
    fi
  done
  [ -n "$ICON_WIN" ] && break
  sleep 2
done

status=0

if [ -z "$WIN" ]; then
  echo "  FAIL  no window with WM_CLASS \"$EXPECTED_CLASS\" appeared within ${DEADLINE_SECS}s"
  dump_tree
  exit 1
fi

echo "== matched window $WIN (icon-bearing: ${ICON_WIN:-none})"
echo "  PASS  WM_CLASS is the bundle id (g_set_prgname took effect)"

TARGET="${ICON_WIN:-$WIN}"
ICON_RAW="$(x xprop -id "$TARGET" _NET_WM_ICON || true)"
if [ -z "$ICON_RAW" ] || echo "$ICON_RAW" | grep -q "not found"; then
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

[ "$status" -ne 0 ] && dump_tree
exit "$status"
