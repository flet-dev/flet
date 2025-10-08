import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class WebviewWeb extends StatelessWidget {
  final Control control;

  const WebviewWeb({super.key, required this.control});
  @override
  Widget build(BuildContext context) {
    return const ErrorControl("Webview is not yet supported on this platform.");
  }
}
