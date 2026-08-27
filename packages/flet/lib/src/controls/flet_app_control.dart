import 'package:flutter/material.dart';

import '../embedded_dart_bridge.dart';
import '../flet_app.dart';
import '../flet_app_errors_handler.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../widgets/embedded_app_scope.dart';
import 'base_controls.dart';

class FletAppControl extends StatefulWidget {
  final Control control;

  FletAppControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<FletAppControl> createState() => _FletAppControlState();
}

class _FletAppControlState extends State<FletAppControl> {
  final _errorsHandler = FletAppErrorsHandler();
  EmbeddedDartBridge? _dartBridge;

  @override
  void initState() {
    super.initState();
    // When this embedded app is addressed as `dartbridge://`, run it over an
    // in-process dart_bridge channel instead of a socket. The native port is
    // Dart-allocated, so we allocate it here and hand it to the host's Python
    // via a `connect` control event — the host then serves that port with a
    // FletDartBridgeServer. The embedded backend's send-retry loop covers the
    // window until the server registers. Falls back to the URL transport when
    // dart_bridge isn't available (web / desktop dev): _dartBridge stays null.
    final url = widget.control.getString("url", "")!;
    if (url.startsWith("dartbridge://") && embeddedDartBridgeConnector != null) {
      final bridge = embeddedDartBridgeConnector!();
      _dartBridge = bridge;
      widget.control.triggerEvent("connect", bridge.port);
    }
  }

  @override
  void dispose() {
    _dartBridge?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FletApp build: ${widget.control.id}");

    var url = widget.control.getString("url", "")!;
    // Multiple embedded FletApps on the same page (e.g. a Preview inside
    // another Flet app) each leave `url` empty, which collides in the
    // JS-side worker registry keyed on `address`. Synthesize a unique
    // address from the control id so each backend channel is its own.
    if (url.isEmpty) {
      url = "embedded:${widget.control.id}";
    }
    var reconnectIntervalMs = widget.control.getInt("reconnect_interval_ms");
    var reconnectTimeoutMs = widget.control.getInt("reconnect_timeout_ms");
    var bootScreenName = widget.control.getString("boot_screen_name", "flet")!;
    var rawBootScreenOptions = widget.control.get("boot_screen_options");
    var bootScreenOptions = rawBootScreenOptions is Map
        ? Map<String, dynamic>.from(rawBootScreenOptions)
        : <String, dynamic>{};
    var appErrorMessage = widget.control.getString("app_error_message");

    Widget app = FletApp(
        controlId: widget.control.id,
        reconnectIntervalMs: reconnectIntervalMs,
        reconnectTimeoutMs: reconnectTimeoutMs,
        bootScreenName: bootScreenName,
        bootScreenOptions: bootScreenOptions,
        appErrorMessage: appErrorMessage,
        pageUrl: url,
        assetsDir: widget.control.getString("assets_dir", "")!,
        errorsHandler: _errorsHandler,
        extensions: FletBackend.of(context).extensions,
        // In-process dart_bridge transport for `dartbridge://` embedded apps;
        // null otherwise, so FletApp uses its URL-scheme channel factory.
        channelBuilder: _dartBridge?.channelBuilder,
        dataChannelFactory: _dartBridge?.dataChannelFactory,
        args: widget.control.get("args") != null
            ? Map<String, dynamic>.from(widget.control.get("args"))
            : null,
        forcePyodide: widget.control.getBool("force_pyodide"),
    );

    // Scope the embedded app's MediaQuery to *this widget's* box.
    //
    // Without this the guest inherits the host window's MediaQuery, so
    // `PageMedia` reports the host's size as the guest's `page.width`/`height`
    // and fires `on_resize` with it - a 393x852 phone preview believes it is
    // as big as the window around it. `size` also decides
    // `MediaQuery.orientation`, so portrait/landscape follows from it.
    //
    // `media_padding`, when set, additionally overrides what the guest sees as
    // its safe-area insets: `padding` is what SafeArea and `page.media.padding`
    // read, and `viewPadding` is the same thing ignoring viewInsets, so the two
    // are kept consistent.
    var mediaPadding = widget.control.getPadding("media_padding");
    final inner = app;
    app = LayoutBuilder(
      builder: (ctx, constraints) {
        var media = MediaQuery.of(ctx);
        // Unbounded constraints would make a nonsense size; leave the
        // inherited one alone in that case.
        if (constraints.biggest.isFinite) {
          media = media.copyWith(size: constraints.biggest);
        }
        if (mediaPadding != null) {
          media = media.copyWith(
              padding: mediaPadding, viewPadding: mediaPadding);
        }
        return MediaQuery(data: media, child: inner);
      },
    );

    return LayoutControl(
      control: widget.control,
      child: EmbeddedAppScope(
        route: widget.control.getString("route"),
        window: widget.control.get("window_state") is Map
            ? Map<String, dynamic>.from(widget.control.get("window_state"))
            : null,
        onWindowAction: (name, args) => widget.control
            .triggerEvent("window_event", {"action": name, "data": args}),
        onRouteChanged: (r) {
          // Guarded so the write-back does not bounce straight back down as a
          // push; EmbeddedAppScope compares routes on the way in too.
          if (r == widget.control.getString("route")) return;
          widget.control.updateProperties({"route": r});
          widget.control.triggerEvent("route_change", r);
        },
        onTitleChanged: (t) {
          if (t == widget.control.getString("title")) return;
          widget.control.updateProperties({"title": t});
          widget.control.triggerEvent("title_change", t);
        },
        child: app,
      ),
    );
  }
}
