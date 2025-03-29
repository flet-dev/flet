import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'controls/control_widget.dart';
import 'flet_app_errors_handler.dart';
import 'flet_backend.dart';
import 'flet_extension.dart';
import 'models/control.dart';

/// FletApp - The top-level widget that initializes everything
class FletApp extends StatefulWidget {
  final String pageUrl;
  final String assetsDir;
  final bool? showAppStartupScreen;
  final String? appStartupScreenMessage;
  final int? controlId;
  final String? title;
  final FletAppErrorsHandler? errorsHandler;
  final int? reconnectIntervalMs;
  final int? reconnectTimeoutMs;
  final List<FletExtension>? extensions;

  const FletApp(
      {super.key,
      required this.pageUrl,
      required this.assetsDir,
      this.showAppStartupScreen,
      this.appStartupScreenMessage,
      this.controlId,
      this.title,
      this.errorsHandler,
      this.reconnectIntervalMs,
      this.reconnectTimeoutMs,
      this.extensions});

  @override
  State<FletApp> createState() => _FletAppState();
}

class _FletAppState extends State<FletApp> {
  FletBackend? backend;

  @override
  void deactivate() {
    backend?.disconnect();
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<FletBackend>(
      create: (context) {
        return FletBackend(
            showAppStartupScreen: widget.showAppStartupScreen,
            appStartupScreenMessage: widget.appStartupScreenMessage,
            controlId: widget.controlId,
            reconnectIntervalMs: widget.reconnectIntervalMs,
            reconnectTimeoutMs: widget.reconnectTimeoutMs,
            pageUri: Uri.parse(widget.pageUrl),
            assetsDir: widget.assetsDir,
            errorsHandler: widget.errorsHandler,
            extensions: widget.extensions ?? [],
            parentFletBackend:
                Provider.of<FletBackend?>(context, listen: false));
      },
      child: Selector<FletBackend, Control>(
        selector: (_, backend) => backend.page,
        builder: (_, page, __) => ControlWidget(control: page),
      ),
    );
  }
}
