import 'package:flet_view/flet_app_services.dart';
import 'package:flutter/material.dart';

import 'flet_app_main.dart';

class FletApp extends StatelessWidget {
  final String pageUrl;
  final String sessionId;
  final String? title;

  const FletApp(
      {Key? key, required this.pageUrl, required this.sessionId, this.title})
      : super(key: key);

  @override
  Widget build(BuildContext context) => FletAppServices(
      child: FletAppMain(title: title ?? "Flet"),
      pageUrl: pageUrl,
      sessionId: sessionId);
}
