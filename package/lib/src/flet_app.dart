import 'package:flutter/material.dart';

import 'flet_app_errors_handler.dart';
import 'flet_app_main.dart';
import 'flet_app_services.dart';

class FletApp extends StatefulWidget {
  final String pageUrl;
  final String? title;
  final FletAppErrorsHandler? errorsHandler;

  const FletApp(
      {Key? key, required this.pageUrl, this.title, this.errorsHandler})
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
          errorsHandler: widget.errorsHandler,
          child: FletAppMain(title: widget.title ?? "Flet"));
    }
    return _appServices!;
  }
}
