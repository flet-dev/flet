import 'package:flutter/material.dart';

import '../flet_app.dart';
import '../flet_app_errors_handler.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import 'create_control.dart';

class FletAppControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const FletAppControl(
      {super.key, required this.parent, required this.control});

  @override
  State<FletAppControl> createState() => _FletAppControlState();
}

class _FletAppControlState extends State<FletAppControl> {
  final _errorsHandler = FletAppErrorsHandler();

  @override
  Widget build(BuildContext context) {
    debugPrint("FletApp build: ${widget.control.id}");

    var url = widget.control.getString("url", "")!;
    var reconnectIntervalMs = widget.control.getInt("reconnectIntervalMs");
    var reconnectTimeoutMs = widget.control.getInt("reconnectTimeoutMs");
    var showAppStartupScreen = widget.control.getBool("showAppStartupScreen");
    var appStartupScreenMessage =
        widget.control.getString("appStartupScreenMessage");

    return constrainedControl(
        context,
        FletApp(
          controlId: widget.control.id,
          reconnectIntervalMs: reconnectIntervalMs,
          reconnectTimeoutMs: reconnectTimeoutMs,
          showAppStartupScreen: showAppStartupScreen,
          appStartupScreenMessage: appStartupScreenMessage,
          pageUrl: url,
          assetsDir: "",
          errorsHandler: _errorsHandler,
          createControlFactories:
              FletAppServices.of(context).createControlFactories,
        ),
        widget.parent,
        widget.control);
  }
}
