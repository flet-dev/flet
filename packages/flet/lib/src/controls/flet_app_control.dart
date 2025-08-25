import 'package:flutter/material.dart';

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

  @override
  Widget build(BuildContext context) {
    debugPrint("FletApp build: ${widget.control.id}");

    var url = widget.control.getString("url", "")!;
    var reconnectIntervalMs = widget.control.getInt("reconnect_interval_ms");
    var reconnectTimeoutMs = widget.control.getInt("reconnect_timeout_ms");
    var showAppStartupScreen =
        widget.control.getBool("show_app_startup_screen");
    var appStartupScreenMessage =
        widget.control.getString("app_startup_screen_message");

    return LayoutControl(
      control: widget.control,
      child: FletApp(
        controlId: widget.control.id,
        reconnectIntervalMs: reconnectIntervalMs,
        reconnectTimeoutMs: reconnectTimeoutMs,
        showAppStartupScreen: showAppStartupScreen,
        appStartupScreenMessage: appStartupScreenMessage,
        pageUrl: url,
        assetsDir: "",
        errorsHandler: _errorsHandler,
        extensions: FletBackend.of(context).extensions,
        args: widget.control.get("args") != null
            ? Map<String, dynamic>.from(widget.control.get("args"))
            : null,
        forcePyodide: widget.control.getBool("force_pyodide"),
      ),
    );
  }
}
