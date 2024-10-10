import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class WebviewWeb extends StatefulWidget {
  final Control control;
  final FletControlBackend backend;

  const WebviewWeb({super.key, required this.control, required this.backend});
  @override
  State<WebviewWeb> createState() => _WebviewWebState();
}

class _WebviewWebState extends State<WebviewWeb> {
  @override
  Widget build(BuildContext context) {
    return const ErrorControl("Webview is not yet supported on this platform.");
  }
}
