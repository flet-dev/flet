import 'package:flutter/material.dart';

import 'flet_app_errors_handler.dart';
import 'flet_app_main.dart';
import 'flet_app_services.dart';
import 'models/control.dart';
import 'models/control_view_model.dart';

class FletApp extends StatefulWidget {
  final String pageUrl;
  final String assetsDir;
  final Map<String, Widget Function(Control?, ControlViewModel)>?
      controlsMapping;
  final String? title;
  final FletAppErrorsHandler? errorsHandler;

  const FletApp(
      {Key? key,
      required this.pageUrl,
      required this.assetsDir,
      this.controlsMapping,
      this.title,
      this.errorsHandler})
      : super(key: key);

  @override
  State<FletApp> createState() => _FletAppState();
}

class _FletAppState extends State<FletApp> {
  String? _pageUrl;
  FletAppServices? _appServices;

  @override
  void dispose() {
    _appServices?.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.pageUrl != _pageUrl) {
      _pageUrl = widget.pageUrl;
      _appServices = FletAppServices(
          pageUrl: widget.pageUrl,
          assetsDir: widget.assetsDir,
          controlsMapping: widget.controlsMapping,
          errorsHandler: widget.errorsHandler,
          child: FletAppMain(title: widget.title ?? "Flet"));
    }
    return _appServices!;
  }
}
