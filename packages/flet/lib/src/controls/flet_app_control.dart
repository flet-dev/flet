import 'package:flutter/material.dart';

import '../embedded_dart_bridge.dart';
import '../flet_app.dart';
import '../flet_app_errors_handler.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
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

    return LayoutControl(
      control: widget.control,
      child: FletApp(
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
      ),
    );
  }
}
