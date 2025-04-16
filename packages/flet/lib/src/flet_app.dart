import 'package:flutter/material.dart';

import 'control_factory.dart';
import 'flet_app_errors_handler.dart';
import 'flet_app_main.dart';
import 'flet_app_services.dart';

class FletApp extends StatefulWidget {
  final String pageUrl;
  final String assetsDir;
  final bool? showAppStartupScreen;
  final String? appStartupScreenMessage;
  final String? controlId;
  final String? title;
  final FletAppErrorsHandler? errorsHandler;
  final int? reconnectIntervalMs;
  final int? reconnectTimeoutMs;
  final List<CreateControlFactory>? createControlFactories;

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
      this.createControlFactories});

  @override
  State<FletApp> createState() => _FletAppState();
}

class _FletAppState extends State<FletApp> {
  String? _pageUrl;
  FletAppServices? _appServices;

  @override
  void deactivate() {
    _appServices?.close();
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.pageUrl != _pageUrl) {
      _pageUrl = widget.pageUrl;
      _appServices = FletAppServices(
          parentAppServices: FletAppServices.maybeOf(context),
          showAppStartupScreen: widget.showAppStartupScreen,
          appStartupScreenMessage: widget.appStartupScreenMessage,
          controlId: widget.controlId,
          reconnectIntervalMs: widget.reconnectIntervalMs,
          reconnectTimeoutMs: widget.reconnectTimeoutMs,
          pageUrl: widget.pageUrl,
          assetsDir: widget.assetsDir,
          errorsHandler: widget.errorsHandler,
          createControlFactories: widget.createControlFactories ?? [],
          child: FletAppMain(title: widget.title ?? "Flet"));
    }
    return _appServices!;
  }
}
