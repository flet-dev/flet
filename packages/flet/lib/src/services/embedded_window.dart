import '../models/control.dart';

/// Stands in for the real window service when a Flet app runs as a guest.
///
/// An embedded app has no OS window of its own - the window it appears to live
/// in is drawn by its host. The real service is suppressed for embedded pages
/// (it would drive the *host's* window), so this takes its place and wires
/// `page.window` to the host instead:
///
///  * host to guest - [apply] writes the host's simulated window state onto the
///    guest's `Window` control, so `page.window.width`, `.maximized` and the
///    rest read correctly in the guest's own Python, and raises the matching
///    `window_event` so the guest's `on_event` fires like it would on a desktop.
///  * guest to host - property sets (`page.window.maximized = True`) and method
///    calls (`close()`, `maximize()`, ...) are forwarded to the host as actions.
///    The host decides what to honour, so a preview that cannot minimize simply
///    ignores that action rather than pretending.
///
/// Both directions are guarded against echo: [apply] records what it wrote, and
/// a change that matches the last write is the host's own value coming back,
/// not the guest asking for something.
class EmbeddedWindowService {
  /// The guest's `Window` control.
  final Control control;

  /// Forwards a guest-side request to the host. [name] is a method name
  /// (`close`, `maximize`, ...) or `set` for a property write.
  final void Function(String name, Map<String, dynamic> args) onAction;

  /// Properties mirrored between host and guest. Anything outside this set is
  /// left alone: a guest can still hold it, it just means nothing here.
  static const mirrored = [
    "width",
    "height",
    "top",
    "left",
    "maximized",
    "minimized",
    "full_screen",
    "focused",
    // Capabilities, not state: an app turns its own buttons off with
    // `page.window.maximizable = False`, and the host draws the chrome to
    // match. There is no UI for this because a real window has none.
    "minimizable",
    "maximizable",
    "resizable",
    "movable",
    "frameless",
    "title_bar_hidden",
    "title_bar_buttons_hidden",
    "prevent_close",
    "visible",
    "min_width",
    "min_height",
    "max_width",
    "max_height",
  ];

  /// Host-initiated one-shot events, which are not window *state* and so have
  /// no mirrored property. The host bumps a counter; a change raises the event.
  /// `close_request` is how `prevent_close` works: the host asks instead of
  /// closing, and the app decides.
  static const requests = {"close_request": "close"};

  final Map<String, dynamic> _applied = {};
  bool _applying = false;

  EmbeddedWindowService({required this.control, required this.onAction}) {
    control.addInvokeMethodListener(_invokeMethod);
    control.addListener(_onControlUpdated);
  }

  void dispose() {
    control.removeInvokeMethodListener(_invokeMethod);
    control.removeListener(_onControlUpdated);
  }

  /// Push the host's window state onto the guest and raise the events it implies.
  void apply(Map<String, dynamic>? state) {
    if (state == null) {
      return;
    }
    // One-shot requests first: they carry no state, so they are compared and
    // consumed here rather than written onto the control.
    requests.forEach((key, event) {
      if (state.containsKey(key) && _applied[key] != state[key]) {
        final first = !_applied.containsKey(key);
        _applied[key] = state[key];
        if (!first) {
          _raise(event);
        }
      }
    });

    final changes = <String, dynamic>{};
    for (var key in mirrored) {
      if (!state.containsKey(key)) {
        continue;
      }
      final value = state[key];
      if (_applied[key] != value) {
        changes[key] = value;
      }
    }
    if (changes.isEmpty) {
      return;
    }

    _applying = true;
    try {
      _applied.addAll(changes);
      control.updateProperties(changes);
    } finally {
      _applying = false;
    }

    // Same contract as FletBackend.onWindowEvent: the event is named "event"
    // (the Python property is `Window.on_event`) and its payload is a map with
    // a `type` key, because WindowEvent has a typed `type` field rather than a
    // raw payload. A bare string arrives as `data == null`.
    //
    // The names must be WindowEventType values - note the hyphens in the
    // full-screen ones.
    if (changes.containsKey("width") || changes.containsKey("height")) {
      _raise("resize");
    }
    if (changes.containsKey("top") || changes.containsKey("left")) {
      _raise("move");
    }
    if (changes.containsKey("maximized")) {
      _raise(changes["maximized"] == true ? "maximize" : "unmaximize");
    }
    if (changes.containsKey("minimized")) {
      _raise(changes["minimized"] == true ? "minimize" : "restore");
    }
    if (changes.containsKey("full_screen")) {
      _raise(changes["full_screen"] == true
          ? "enter-full-screen"
          : "leave-full-screen");
    }
    if (changes.containsKey("focused")) {
      _raise(changes["focused"] == true ? "focus" : "blur");
    }
    if (changes.containsKey("visible")) {
      _raise(changes["visible"] == true ? "show" : "hide");
    }
  }

  void _raise(String type) => control.triggerEvent("event", {"type": type});

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    onAction(name, args is Map ? Map<String, dynamic>.from(args) : {});
    return null;
  }

  void _onControlUpdated() {
    if (_applying) {
      return;
    }
    // Anything that differs from the last value we wrote is the guest asking
    // for a change, so hand it to the host to accept or ignore.
    final wanted = <String, dynamic>{};
    for (var key in mirrored) {
      final value = control.get(key);
      if (value != null && _applied[key] != value) {
        _applied[key] = value;
        wanted[key] = value;
      }
    }
    if (wanted.isNotEmpty) {
      onAction("set", wanted);
    }
  }
}
