import 'flet_app_services.dart';
import 'package:flutter/material.dart';

import 'flet_app_main.dart';

class FletApp extends StatelessWidget {
  final String pageUrl;
  final String? title;

  const FletApp({Key? key, required this.pageUrl, this.title})
      : super(key: key);

  @override
  Widget build(BuildContext context) => FletAppServices(
      pageUrl: pageUrl, child: FletAppMain(title: title ?? "Flet"));
}
