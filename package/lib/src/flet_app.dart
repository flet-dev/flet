import 'package:flutter/material.dart';

import 'flet_app_errors_handler.dart';
import 'flet_app_main.dart';
import 'flet_app_services.dart';

class FletApp extends StatelessWidget {
  final String pageUrl;
  final String? title;
  final FletAppErrorsHandler? errorsHandler;

  const FletApp(
      {Key? key, required this.pageUrl, this.title, this.errorsHandler})
      : super(key: key);

  @override
  Widget build(BuildContext context) => FletAppServices(
      pageUrl: pageUrl,
      errorsHandler: errorsHandler,
      child: FletAppMain(title: title ?? "Flet"));
}
